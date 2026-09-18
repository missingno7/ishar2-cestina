// Native Win32 installer. All embedded game-related data are changed bytes.
#ifndef UNICODE
#define UNICODE
#endif
#define _UNICODE
#define NOMINMAX
#include <windows.h>
#include <bcrypt.h>
#include <shobjidl.h>
#include <shellapi.h>
#include <algorithm>
#include <array>
#include <deque>
#include <filesystem>
#include <fstream>
#include <map>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
#include <cstdio>
#include "patch_data.h"
using Bytes=std::vector<unsigned char>;
using Hash=std::array<unsigned char,32>;
namespace fs=std::filesystem;
static void require(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
static std::wstring wide(const std::string& s){int n=MultiByteToWideChar(CP_UTF8,0,s.data(),(int)s.size(),nullptr,0);std::wstring r(n,0);MultiByteToWideChar(CP_UTF8,0,s.data(),(int)s.size(),r.data(),n);return r;}
static Hash hash(const Bytes& b){
    BCRYPT_ALG_HANDLE a=nullptr;BCRYPT_HASH_HANDLE h=nullptr;Hash r{};
    require(BCryptOpenAlgorithmProvider(&a,BCRYPT_SHA256_ALGORITHM,nullptr,0)>=0,"Nelze otevřít SHA-256.");
    NTSTATUS status=BCryptCreateHash(a,&h,nullptr,0,nullptr,0,0);
    if(status>=0)status=BCryptHashData(h,const_cast<PUCHAR>(b.data()),(ULONG)b.size(),0);
    if(status>=0)status=BCryptFinishHash(h,r.data(),32,0);
    if(h)BCryptDestroyHash(h);BCryptCloseAlgorithmProvider(a,0);
    require(status>=0,"Selhala kontrola SHA-256.");return r;
}
static std::string hex(const Hash& h){const char* chars="0123456789abcdef";std::string s;for(auto b:h){s+=chars[b>>4];s+=chars[b&15];}return s;}
static void regular(const fs::path& p){DWORD a=GetFileAttributesW(p.c_str());require(a!=INVALID_FILE_ATTRIBUTES&&!(a&(FILE_ATTRIBUTE_DIRECTORY|FILE_ATTRIBUTE_REPARSE_POINT)),"Chybí soubor nebo jde o odkaz místo běžného souboru.");}
static Bytes read(const fs::path& p){
    regular(p);HANDLE f=CreateFileW(p.c_str(),GENERIC_READ,FILE_SHARE_READ,nullptr,OPEN_EXISTING,0,nullptr);
    require(f!=INVALID_HANDLE_VALUE,"Soubor nelze otevřít. Ukončete hru a zkontrolujte přístupová práva.");
    LARGE_INTEGER size;bool ok=GetFileSizeEx(f,&size)&&size.QuadPart>=0&&size.QuadPart<=8*1024*1024;
    Bytes b(ok?(size_t)size.QuadPart:0);DWORD got=0;
    if(ok)ok=ReadFile(f,b.data(),(DWORD)b.size(),&got,nullptr)&&got==b.size();CloseHandle(f);
    require(ok,"Soubor nelze přečíst nebo má neplatnou velikost.");return b;
}
static void writeNew(const fs::path& p,const Bytes& b){
    HANDLE f=CreateFileW(p.c_str(),GENERIC_WRITE,0,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
    require(f!=INVALID_HANDLE_VALUE,"Nelze vytvořit pracovní soubor nebo zálohu. Zkontrolujte právo zápisu.");
    DWORD n=0;bool ok=WriteFile(f,b.data(),(DWORD)b.size(),&n,nullptr)&&n==b.size();
    if(ok)ok=FlushFileBuffers(f);CloseHandle(f);
    if(!ok)DeleteFileW(p.c_str());require(ok,"Zápis selhal. Zkontrolujte volné místo na disku.");
}
struct Hunk{size_t offset;Bytes data;};
struct Patch{std::wstring name;Hash original,target,base;size_t length;std::vector<Hunk> hunks;};
static std::vector<Patch> patches(){
    size_t at=8;require(sizeof(patchData)>=12&&!memcmp(patchData,"ISHCS005",8),"Neplatný patch.");
    auto number=[&](){require(at+4<=sizeof(patchData),"Neúplný patch.");uint32_t n=0;for(int i=0;i<4;i++)n|=uint32_t(patchData[at++])<<(i*8);return n;};
    auto gethash=[&](){require(at+32<=sizeof(patchData),"Neúplný hash.");Hash h;std::copy_n(patchData+at,32,h.begin());at+=32;return h;};
    std::vector<Patch> rows;size_t count=number();require(count==9,"Neplatný počet prostředků.");
    while(count--){Patch p;size_t n=number();require(n<32&&at+n<=sizeof(patchData),"Neplatné jméno.");
        for(size_t i=0;i<n;i++){char c=patchData[at++];require((c>='A'&&c<='Z')||c=='.',"Neplatné jméno.");p.name+=c;}
        p.original=gethash();p.target=gethash();p.base=gethash();p.length=number();size_t k=number();
        require(p.length<=2*1024*1024&&k<=p.length,"Neplatný rozsah.");
        while(k--){Hunk h;h.offset=number();n=number();require(h.offset+n<=p.length&&at+n<=sizeof(patchData),"Neplatný blok.");h.data.assign(patchData+at,patchData+at+n);at+=n;p.hunks.push_back(h);}rows.push_back(p);
    }require(at==sizeof(patchData),"Nadbytečná data patche.");return rows;
}
static size_t header(const Bytes& b){require(b.size()>=6,"Krátká hlavička.");return b[4]==0&&b[5]==0?22:6;}
static Bytes decode(const Bytes& data,size_t declared){
    size_t h=header(data);require(data.size()>=h+8&&data[3]==0xa1,"Nepodporovaná komprese.");
    require((size_t(data[0])|(size_t(data[1])<<8)|(size_t(data[2])<<16))==declared,"Chybná délka prostředku.");
    Bytes out(data.begin(),data.begin()+h);size_t bit=(h+8)*8;
    auto bits=[&](int n){require(n<=16&&bit+n<=(data.size()+16)*8,"Neplatný komprimovaný proud.");unsigned v=0;while(n--){v=(v<<1)|(bit/8<data.size()?((data[bit/8]>>(7-bit%8))&1):0);bit++;}return v;};
    while(out.size()<declared){
        if(bits(1)){size_t n=1;unsigned x;do{x=bits(2);n+=x;require(n<=65535,"Příliš dlouhý literál.");}while(x==3);
            while(n--&&out.size()<declared)out.push_back((unsigned char)bits(8));
            if(out.size()==declared)break;
        }
        unsigned mode=bits(3);size_t distance=bits(data[h+mode])+1,n=(mode&3)+1;
        if(!(mode&3)){n=5;unsigned x;do{x=bits(3);n+=x;require(n<=65535,"Příliš dlouhá shoda.");}while(x==7);}
        require(distance<=out.size()-h,"Neplatná zpětná reference.");
        while(n--&&out.size()<declared)out.push_back(out[out.size()-distance]);
    }return out;
}
static Bytes pack(const Bytes& raw){
    const int widths[]={11,9,10,11,7,5,6,7};size_t h=header(raw);
    Bytes src(raw.begin()+h,raw.end()),out(raw.begin(),raw.begin()+h);out[3]=0xa1;for(int w:widths)out.push_back(w);
    uint32_t acc=0;int nbits=0;
    auto put=[&](uint32_t value,int n){acc=(acc<<n)|value;nbits+=n;while(nbits>=8){nbits-=8;out.push_back((acc>>nbits)&255);acc&=(1u<<nbits)-1;}};
    auto groups=[&](size_t count,int bits){size_t limit=(1u<<bits)-1;while(count>=limit){put((uint32_t)limit,bits);count-=limit;}put((uint32_t)count,bits);};
    std::map<unsigned,std::deque<size_t>> history;
    auto key=[&](size_t p){return unsigned(src[p])*256+src[p+1];};
    auto remember=[&](size_t p){if(p+1<src.size()){auto& q=history[key(p)];q.push_back(p);if(q.size()>64)q.pop_front();}};
    struct Match{int mode=-1;size_t distance=0,length=0;};
    auto match=[&](size_t p){Match best;int gain=0;if(p+1>=src.size())return best;auto it=history.find(key(p));if(it==history.end())return best;
        for(auto at=it->second.rbegin();at!=it->second.rend();++at){size_t prev=*at,distance=p-prev;if(distance>2048)break;
            size_t count=2,limit=std::min<size_t>(512,src.size()-p);while(count<limit&&src[prev+count]==src[p+count])count++;
            for(int mode=0;mode<8;mode++){if(distance>(1u<<widths[mode]))continue;size_t length=mode%4==0?count:size_t(mode%4+1);
                if(length>count||(mode%4==0&&count<5))continue;
                int cost=3+widths[mode]+(mode%4==0?3*int((length-5)/7+1):0),saving=8*int(length)-cost;
                if(saving>gain){best={mode,distance,length};gain=saving;}
            }
        }return best;};
    size_t pos=0;
    while(pos<src.size()){size_t begin=pos;auto found=match(pos);
        while(pos<src.size()&&found.mode<0){remember(pos);pos++;found=match(pos);}
        size_t count=pos-begin;require(count<=65535,"Příliš dlouhý komprimovaný literál.");put(count?1:0,1);
        if(count){groups(count-1,2);for(size_t i=begin;i<pos;i++)put(src[i],8);}
        if(pos==src.size())break;
        put(found.mode,3);put((uint32_t)found.distance-1,widths[found.mode]);if(found.mode%4==0)groups(found.length-5,3);
        for(size_t i=pos;i<pos+found.length;i++)remember(i);pos+=found.length;
    }
    if(nbits)out.push_back(acc<<(8-nbits));out.insert(out.end(),4,0);return out;
}
static Bytes applyPatch(const Bytes& input,const Patch& p){
    require(input.size()>=6,"Krátký prostředek.");
    size_t originalLength=size_t(input[0])|(size_t(input[1])<<8)|(size_t(input[2])<<16);
    require(originalLength<=p.length&&p.length<=8*1024*1024,"Neplatná cílová délka.");
    Bytes raw=decode(input,originalLength);require(hash(raw)==p.base,"Rozbalená data neodpovídají podporované verzi.");
    raw.resize(p.length,0);
    for(const auto& h:p.hunks)std::copy(h.data.begin(),h.data.end(),raw.begin()+h.offset);
    Bytes result=(raw[3]&128)?pack(raw):raw;
    require(hash(result)==p.target,"Výsledek patche neprošel kontrolou. Hra nebyla změněna.");return result;
}
struct Stage{
    fs::path path;std::vector<fs::path> files;
    explicit Stage(const fs::path& root){GUID id;require(SUCCEEDED(CoCreateGuid(&id)),"Nelze vytvořit pracovní adresář.");wchar_t text[40];StringFromGUID2(id,text,40);path=root/(std::wstring(L".ishar2-cs-stage-")+text);require(CreateDirectoryW(path.c_str(),nullptr),"Nelze zapisovat do složky hry.");}
    fs::path file(const std::wstring& name){fs::path p=path/name;files.push_back(p);return p;}
    ~Stage(){for(const auto& f:files)DeleteFileW(f.c_str());RemoveDirectoryW(path.c_str());}
};
static void validateExe(const fs::path& root){require(hex(hash(read(root/L"START.EXE")))==supportedExeHash,"Tato verze START.EXE není podporovaná. Hra nebyla změněna.");}
struct DirectoryLock{
    HANDLE handle=INVALID_HANDLE_VALUE;
    DirectoryLock(const fs::path& root,bool needed){if(!needed)return;
        auto p=root/L".ishar2-cs-lock";
        handle=CreateFileW(p.c_str(),GENERIC_WRITE,0,nullptr,CREATE_NEW,FILE_ATTRIBUTE_TEMPORARY|FILE_FLAG_DELETE_ON_CLOSE,nullptr);
        require(handle!=INVALID_HANDLE_VALUE,"Složku nelze uzamknout pro zápis. Zavřete druhý instalátor a ověřte právo zápisu. Po přerušení napájení může zůstat soubor .ishar2-cs-lock.");
    }
    ~DirectoryLock(){if(handle!=INVALID_HANDLE_VALUE)CloseHandle(handle);}
};
static std::wstring run(const fs::path& root,const std::wstring& action){
    require(action==L"--apply"||action==L"--restore"||action==L"--check","Neznámý příkaz.");
    validateExe(root);DirectoryLock lock(root,action!=L"--check");auto rows=patches();std::vector<Bytes> before,after,originals;
    bool allOriginal=true,allTarget=true;
    for(const auto& p:rows){auto data=read(root/p.name);auto h=hash(data);bool a=h==p.original,b=h==p.target;
        if(!a&&!b)throw std::runtime_error("Nepodporovaný nebo změněný soubor: "+std::string(p.name.begin(),p.name.end())+". Hra nebyla změněna.");
        allOriginal&=a;allTarget&=b;before.push_back(std::move(data));
    }
    if(action==L"--check")return allTarget?L"Čeština z tohoto balíčku je již nainstalovaná.":allOriginal?L"Verze hry je podporovaná. Češtinu lze aplikovat.":L"Instalace je částečná. Lze ji dokončit nebo obnovit ze zálohy.";
    if(action==L"--apply"&&allTarget)return L"Čeština z tohoto balíčku je již nainstalovaná. Ve hře vyberte jazyk 3.";
    const fs::path backup=root/backupFolder;
    DWORD attr=GetFileAttributesW(backup.c_str());
    require(attr==INVALID_FILE_ATTRIBUTES||((attr&FILE_ATTRIBUTE_DIRECTORY)&&!(attr&FILE_ATTRIBUTE_REPARSE_POINT)),"Záloha není běžný adresář.");
    if(action==L"--restore")require(attr!=INVALID_FILE_ATTRIBUTES,"Původní záloha chybí. Obnovení není možné.");
    // Verify every existing backup and every input before creating any files.
    for(size_t i=0;i<rows.size();i++){
        const auto& p=rows[i];fs::path path=backup/p.name;
        if(GetFileAttributesW(path.c_str())!=INVALID_FILE_ATTRIBUTES){auto b=read(path);require(hash(b)==p.original,"Záloha je změněná nebo neodpovídá originálu.");originals.push_back(std::move(b));}
        else{require(action!=L"--restore"&&hash(before[i])==p.original,"Chybí část původní zálohy. Nelze bezpečně pokračovat.");originals.push_back(before[i]);}
        after.push_back(action==L"--restore"?originals.back():applyPatch(originals.back(),p));
    }
    Stage stage(root);std::vector<fs::path> staged,rollback;
    for(size_t i=0;i<rows.size();i++){
        auto path=stage.file(rows[i].name);writeNew(path,after[i]);require(hash(read(path))==hash(after[i]),"Pracovní soubor je poškozený.");staged.push_back(path);
        auto old=stage.file(rows[i].name+L".rollback");writeNew(old,before[i]);rollback.push_back(old);
    }
    if(attr==INVALID_FILE_ATTRIBUTES)require(CreateDirectoryW(backup.c_str(),nullptr),"Nelze vytvořit zálohu.");
    for(size_t i=0;i<rows.size();i++){
        auto path=backup/rows[i].name;
        if(GetFileAttributesW(path.c_str())==INVALID_FILE_ATTRIBUTES)writeNew(path,originals[i]);
        require(hash(read(path))==rows[i].original,"Záloha neprošla kontrolou.");
    }
    validateExe(root);for(size_t i=0;i<rows.size();i++)require(read(root/rows[i].name)==before[i],"Herní soubory se během přípravy změnily. Opakujte akci se zavřenou hrou.");
    std::vector<size_t> replaced;
    try{
        for(size_t i=0;i<rows.size();i++){
            if(before[i]==after[i])continue;
            require(MoveFileExW(staged[i].c_str(),(root/rows[i].name).c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH),"Soubor nelze nahradit. Ukončete hru a zkontrolujte přístupová práva.");
            replaced.push_back(i);
#ifdef ISHAR_TESTING
            if(GetEnvironmentVariableW(L"ISHAR_TEST_FAIL_AFTER_FIRST",nullptr,0)&&replaced.size()==1)throw std::runtime_error("Testované selhání zápisu.");
#endif
        }
        for(size_t i=0;i<rows.size();i++)require(hash(read(root/rows[i].name))==hash(after[i]),"Kontrola zapsaných souborů selhala.");
    }catch(const std::exception& error){
        bool ok=true;for(auto i:replaced)if(!MoveFileExW(rollback[i].c_str(),(root/rows[i].name).c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))ok=false;
        if(!ok)throw std::runtime_error("Zápis selhal a návrat nebyl úplný. Originály jsou v záložní složce .ishar2-cs-backup-* ve složce hry. Ukončete hru a použijte Obnovit originál.");
        throw std::runtime_error(std::string(error.what())+" Změny byly vráceny.");
    }
    return action==L"--restore"?L"Původní soubory byly obnoveny. Záloha zůstává zachovaná.":L"Čeština byla úspěšně aplikována. Spusťte hru jako obvykle a vyberte 3 – Čeština.";
}

static HWND pathBox,statusBox,applyButton,restoreButton,browseButton;static bool busy=false;
static constexpr UINT DONE=WM_APP+1;
struct Result{std::wstring text;bool error;};
static void choose(HWND owner){
    IFileDialog* dialog=nullptr;
    if(SUCCEEDED(CoCreateInstance(CLSID_FileOpenDialog,nullptr,CLSCTX_INPROC_SERVER,IID_PPV_ARGS(&dialog)))){
        DWORD flags;dialog->GetOptions(&flags);dialog->SetOptions(flags|FOS_PICKFOLDERS|FOS_FORCEFILESYSTEM|FOS_PATHMUSTEXIST);
        dialog->SetTitle(L"Vyberte složku s START.EXE");
        if(SUCCEEDED(dialog->Show(owner))){IShellItem* item=nullptr;if(SUCCEEDED(dialog->GetResult(&item))){PWSTR p=nullptr;if(SUCCEEDED(item->GetDisplayName(SIGDN_FILESYSPATH,&p))){SetWindowTextW(pathBox,p);CoTaskMemFree(p);}item->Release();}}dialog->Release();
    }
}
static void start(HWND owner,const std::wstring& action){
    int n=GetWindowTextLengthW(pathBox);std::wstring path(n+1,0);GetWindowTextW(pathBox,path.data(),n+1);path.resize(n);
    if(path.empty()){SetWindowTextW(statusBox,L"Nejdříve vyberte složku s hrou.");return;}
    busy=true;for(HWND w:{pathBox,applyButton,restoreButton,browseButton})EnableWindow(w,FALSE);
    SetWindowTextW(statusBox,L"Ověřuji soubory a připravuji změny…");
    std::thread([owner,path,action](){auto result=new Result;try{result->text=run(fs::path(path),action);result->error=false;}catch(const std::exception& e){result->text=wide(e.what());result->error=true;}PostMessageW(owner,DONE,0,(LPARAM)result);}).detach();
}
static LRESULT CALLBACK windowProc(HWND w,UINT message,WPARAM wp,LPARAM lp){
    if(message==WM_COMMAND){switch(LOWORD(wp)){case 101:choose(w);break;case 102:start(w,L"--apply");break;case 103:start(w,L"--restore");break;}return 0;}
    if(message==DONE){auto r=reinterpret_cast<Result*>(lp);SetWindowTextW(statusBox,r->text.c_str());if(r->error)MessageBeep(MB_ICONWARNING);delete r;busy=false;for(HWND c:{pathBox,applyButton,restoreButton,browseButton})EnableWindow(c,TRUE);return 0;}
    if(message==WM_CLOSE){if(!busy)DestroyWindow(w);return 0;}
    if(message==WM_DESTROY){PostQuitMessage(0);return 0;}return DefWindowProcW(w,message,wp,lp);
}
int WINAPI wWinMain(HINSTANCE instance,HINSTANCE,LPWSTR,int show){
    int argc;LPWSTR* argv=CommandLineToArgvW(GetCommandLineW(),&argc);
    if(argc>1){int result=0;try{require(argc==3,"Použití: --check / --apply / --restore a cesta ke hře.");auto text=run(fs::path(argv[2]),argv[1]);fwprintf(stdout,L"%ls\n",text.c_str());}catch(const std::exception& e){fprintf(stderr,"%s\n",e.what());result=1;}LocalFree(argv);return result;}
    LocalFree(argv);CoInitializeEx(nullptr,COINIT_APARTMENTTHREADED);
    WNDCLASSW cls{};cls.hInstance=instance;cls.lpszClassName=L"IsharCestina";cls.lpfnWndProc=windowProc;cls.hCursor=LoadCursor(nullptr,IDC_ARROW);cls.hbrBackground=(HBRUSH)(COLOR_BTNFACE+1);cls.hIcon=LoadIcon(nullptr,IDI_APPLICATION);RegisterClassW(&cls);
    RECT rect{0,0,620,250};AdjustWindowRect(&rect,WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU|WS_MINIMIZEBOX,FALSE);
    HWND w=CreateWindowW(cls.lpszClassName,windowTitle,WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU|WS_MINIMIZEBOX,CW_USEDEFAULT,CW_USEDEFAULT,rect.right-rect.left,rect.bottom-rect.top,nullptr,nullptr,instance,nullptr);
    HFONT font=CreateFontW(-16,0,0,0,FW_NORMAL,FALSE,FALSE,FALSE,DEFAULT_CHARSET,0,0,CLEARTYPE_QUALITY,0,L"Segoe UI");
    auto control=[&](const wchar_t* type,const wchar_t* text,DWORD style,int x,int y,int width,int height,int id){HWND c=CreateWindowExW(type==std::wstring(L"EDIT")?WS_EX_CLIENTEDGE:0,type,text,WS_CHILD|WS_VISIBLE|style,x,y,width,height,w,(HMENU)(INT_PTR)id,instance,nullptr);SendMessageW(c,WM_SETFONT,(WPARAM)font,TRUE);return c;};
    control(L"STATIC",L"Vyberte složku hry obsahující START.EXE:",0,22,20,570,24,0);
    pathBox=control(L"EDIT",L"",WS_TABSTOP|ES_AUTOHSCROLL,22,50,448,29,100);
    browseButton=control(L"BUTTON",L"Vybrat složku…",WS_TABSTOP,480,50,118,29,101);
    applyButton=control(L"BUTTON",L"Aplikovat češtinu",WS_TABSTOP|BS_DEFPUSHBUTTON,22,98,180,36,102);
    restoreButton=control(L"BUTTON",L"Obnovit originál",WS_TABSTOP,216,98,164,36,103);
    statusBox=control(L"STATIC",L"Před použitím ukončete hru. Originály se automaticky zálohují.\r\nČeština nahrazuje němčinu; ve hře ji vyberete číslem 3.",0,22,153,576,76,0);
    ShowWindow(w,show);UpdateWindow(w);SetFocus(browseButton);
    MSG msg;while(GetMessageW(&msg,nullptr,0,0)>0){if(!IsDialogMessageW(w,&msg)){TranslateMessage(&msg);DispatchMessageW(&msg);}}
    DeleteObject(font);CoUninitialize();return 0;
}
