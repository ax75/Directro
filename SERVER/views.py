from django.shortcuts import render, HttpResponse
import subprocess, os


Base_dir = "/media/kenshi/MAIN DRIVE/Multi_Resources/"
osType = os.name.lower()

# Create your views here.

def create_req_url(base_dir):
    f_base_dir = ''

    for x in base_dir:
        if x == '/' and os.name.lower() ==  "nt":
            f_base_dir += '\\'
        else:
            f_base_dir += x

    if base_dir != Base_dir:
        mime_url = os.path.join('all', f_base_dir.replace(Base_dir, ''))
    else:
        mime_url = 'all'
    print(f_base_dir + "  " + mime_url)
    return f_base_dir, mime_url


def create_dir_dict(base_dir, mime_url, contents):
    dir_info = {}
    mimes = {}
    names = []
    tmp = ''

    for x in contents:
        if x !='\n':
            tmp = tmp+x
        else:

            if os.path.isdir(os.path.join(base_dir, tmp).replace('\r', '')):
                dir_info[tmp] = os.path.join(base_dir, tmp)
                print("---------------------------------------------------------------------------------------->>"+tmp)
            else:
                mimes[tmp] = os.path.join(mime_url, tmp)
            tmp = ''
            print(dir_info, mimes)

    return dir_info, mimes, names


def forward_slasher(mimes):

    for name, path in mimes.items():
        mimes[name] = path.replace('\\', '/')

    return mimes


def index(request):
   


    if osType in "posix":
        o_dirs = subprocess.run(['ls', Base_dir], capture_output=True, )
    elif osType in "nt":
        o_dirs = subprocess.run(['dir', Base_dir, '/B'], capture_output=True, )
    else:
        return HttpResponse("Operating System Not Supported...")

    dirs = o_dirs.stdout
    dirs = dirs.decode()

    f_base_dir, mime_url = create_req_url(Base_dir)
    dir_info, mimes, names = create_dir_dict(f_base_dir, mime_url, dirs)

    mimes = forward_slasher(mimes)

    # return HttpResponse(mimes.values())
    print(dirs)

    return render(request, 'SERVER/index.html', {'dir_info': dir_info, 'mimes': mimes, 'base_dir': f_base_dir})


def temp(request, num):
    r = str(request.headers)
    return HttpResponse(r)


def check_dir(request, base_dir):

    f_base_dir, mime_url = create_req_url(base_dir)
    

    if osType in "posix":
        o_dirs = subprocess.run(['ls', f_base_dir], capture_output=True, )
    elif osType in "nt":
        o_dirs = subprocess.run(['dir', f_base_dir, '/B'], capture_output=True, )
    else:
        return HttpResponse("Operating System Not Supported...")

    dirs = o_dirs.stdout
    dirs = dirs.decode()
    dir_info, mimes, names = create_dir_dict(f_base_dir, mime_url, dirs)

    mimes = forward_slasher(mimes)

    #return HttpResponse(mimes.values())
    r = str(request.headers['Referer'])

    return render(request, 'SERVER/index.html', {'dir_info': dir_info, 'mimes': mimes, 'base_dir': f_base_dir, 'r': r})


def testing(request):

    return render(request, 'testing.html')

