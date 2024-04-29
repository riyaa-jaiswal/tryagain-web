import random;
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector
from datetime import date
from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt
mydb=mysql.connector.connect(host="localhost",user="root",password="",database="mppdb");
cur=mydb.cursor();
dt=date.today();
# Create your views here.
def index(request):
    noti="";
    query="SELECT * FROM tbl_notification";
    cur.execute(query);
    res=cur.fetchall();
    noti +="<ul>";
    for i in res:
        noti="<li style='list-style-type:none'>"+i[1]+"</li>";
    noti +="</ul>";
    return render(request,'index.html',{'Noti':noti});
def Gallery(request):
    return render(request,'Gallery.html');
def AboutUs(request):
    return render(request,'AboutUs.html');
def AboutCollege(request):
    return render(request,'AboutCollege.html');
def AboutPrincipal(request):
    return render(request,'AboutPrincipal.html');
def AboutBranch(request):
    return render(request,'AboutBranch.html');
def AboutLibrary(request):
    return render(request,'AboutLibrary.html');
def Facilities(request):
    return render(request,'Facilities.html');
def Faculty(request):
    return render(request,'Faculty.html');
def Registration(request):
    msg="";total="";
    if(request.method=="POST"):
        cph=request.POST.get("txtcaptcha");
        captch=request.POST.get("txtcaptchacode");
        name=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        mob=request.POST.get("txtmobile");
        quali=request.POST.get("ddlqualification");
        passwd=request.POST.get("txtpass");
        cpass=request.POST.get("txtcpass");
        pic=request.FILES["fupic"];
        loc=FileSystemStorage(location='media/');
        filename=loc.save(pic.name,pic);
        fileurl=loc.url(filename);
        if(passwd==cpass):
            if(cph==captch):
                query = "insert into tbl_register values('"+name+"','"+email+"','"+passwd+"','"+mob+"','"+quali+"','"+pic.name+"','"+str(dt)+"')";
                query2="insert into tbl_login values('"+email+"','"+passwd+"','user','"+str(dt)+"')";
                cur.execute(query);
                cur.execute(query2)
                msg="Registration save successfully..";
            else:
                msg="Captcha code not match"
        else:
            msg="password and confirm password not matched!";
    else:
        pass;
    return render(request,'Registration.html',{'Msg':msg,'Total':total});
def ContactUs(request):
    res="";
    if(request.method=="POST"):
        ename=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        mobile=request.POST.get("txtmobile");
        msg=request.POST.get("txtmessage");
        query="insert into tbl_contact(name,email,mobile,msg,edt)values('"+ename+"','"+email+"','"+mobile+"','"+msg+"','"+str(dt)+"')";
        cur.execute(query);
        res="Enquiry Save Successfully ! Arcane team Contact shortly !!";
    return render(request,'ContactUs.html',{'Res':res});
def Login(request):
    msg="";
    if request.method=="POST":
        id=request.POST.get("txtuserid");
        passwd=request.POST.get("txtpassword");
        query="select * from tbl_login where userid='"+id+"' and password='"+passwd+"'";
        cur.execute(query);
        res=cur.fetchall();
        a=cur.rowcount;
        if a>0:
            type=res[0][2];
            if(type=="user"):
                request.session["uid"]=id;
                return redirect("/UserZone/SDashboard");
            elif(type=="admin"):
                request.session["aid"] = id;
            return redirect("/AdminZone/Adashboard");
        else:
            msg="Invalid Userid and password";

    return render(request,'Login.html',{'Msg':msg});
def SDashboard(request):
    return render(request,'UserZone/SDashboard.html');
def Myprofile(request):
    name="";email="";mob="";date="";quali="";msg="";pic="";
    id=request.session.get("uid");
    query="select * from tbl_register where email='"+id+"'";
    cur.execute(query);
    res=cur.fetchall();
    # a=cur.rowcount;
    # if(a>0):
    name=res[0][0];
    email=res[0][1];mob=res[0][3];quali=res[0][4];pi=res[0][5];date=res[0][6];
    if(request.method=="POST"):
        name=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        mob=request.POST.get("txtmobile");
        query="update tbl_register set name='"+name+"',mobile='"+mob+"' where email='"+email+"'";
        cur.execute(query);
        msg="Profile Updated Successfully..";
    return render(request,'UserZone/Myprofile.html',{'Name':name,'Email':email,'Mob':mob,'Quali':quali,'Date':date,'Msg':msg,'Pic':pi});

def Schangepassword(request):
    msg="";
    id=request.session.get("uid");
    if(id==None or id==""):
        return redirect("/login");
    else:
        if(request.method=="POST"):
            id=request.session.get("uid");
            oldpass=request.POST.get("txtoldpass");
            newpass=request.POST.get("txtnewpass");
            cpass=request.POST.get("txtcpass");
            if(newpass==cpass):
                query="update tbl_login set password='"+newpass+"' where userid='"+id+"'and password='"+oldpass+"'";
                cur.execute(query);
                msg="Password Change Successfuly..";
            else:
                msg="New Password and Confirm Password Not Match";
    return render(request,'UserZone/Schangepassword.html');
def feedback(request):
    msg=""
    id=request.session.get("uid");
    if(request.method=="POST"):
        total=request.POST.get("txttotal");
        msg=request.POST.get("txtmsg");
        query="insert into tbl_feedback(userid,rating,msg,fdt) values('"+id+"','"+total+"','"+msg+"','"+str(dt)+"')";
        cur.execute(query);
        msg="Feedback save successfully";
    return render(request,'UserZone/feedback.html',{'Msg':msg});
def logout(request):
    id=request.session.get("uid");
    if(id !=None and id != ""):
        request.session.flush();
        request.session= {};
        return redirect("/Login");
    else:
        return redirect("/Login");
    return render(request,'UserZone/logout.html');
#code for adminzone
def Adashboard(request):
    id=request.session.get("aid");
    if(id!=None and id!=""):
        pass;
    else:
        return redirect("../login");
    return render(request,'AdminZone/Adashboard.html');
def ViewRegistration(request):
    tbl="";
    query="select * from tbl_register";
    cur.execute(query);
    res=cur.fetchall();
    a=cur.rowcount;
    if(a>0):
        tbl+="<table class='table table-responsive' id='example'><thead><tr style='background:orangered;color:white;'><th>name</th><th>email</th><th>password</th><th>mobile</th><th>Qualification</th><th>picture</th><th>Delete</th><th>Update</th></tr></thead>";
        tbl+="<tbody>";
        for i in res:
            tbl+="<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td>"+i[3]+"</td><td>"+i[4]+"</td><td>"+i[5]+"</td><td><a href='/AdminZone/Rdelete?del="+i[1]+"'><span class='fa fa-trash'></span></a></td><td><a href='/AdminZone/Rupdate?up="+i[1]+"'><span class='fa fa-eye'></span></a></td></tr>";
        tbl+="</tbody>";
        tbl+="</table>";
    else:
        msg="No Record Found";
    return render(request,'AdminZone/ViewRegistration.html',{'Tbl':tbl});
def Rdelete(request):
    msg="";
    email=request.GET.get("del");
    query="delete from tbl_register where email='"+email+"'";
    cur.execute(query);
    msg="Delete Data Successfully";
    return render(request,'AdminZone/Rdelete.html',{'Msg':msg});
def Rupdate(request):
    msg="";name="";email="";password="";mobile="";qualification="";picture="";message="";
    email=request.GET.get("up");
    query="select * from tbl_register where email='"+email+"'";
    cur.execute(query);
    res=cur.fetchall();
    a=cur.rowcount;
    if(a>0):
        name=res[0][0];email=res[0][1];password=res[0][2];mobile=res[0][3];qualification=res[0][4];picture=res[0][5];
    if(request.method=="POST"):
        name=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        password=request.POST.get("txtpass");
        mobile=request.POST.get("txtmob");
        qualification=request.POST.get("txtquali");
        picture=request.POST.get("txtpic");
        query="update tbl_register set name='"+name+"',email='"+email+"',password='"+password+"',mobile='"+mobile+"',Qualification='"+qualification+"',Picture='"+picture+"'";
        cur.execute(query);
        message="Update data successfully";
    return render(request,'AdminZone/Rupdate.html',{'Name':name,'Email':email,'Password':password,'Mobile':mobile,'Qualification':qualification,'Picture':picture,'Msg':msg,'Message':message});
def ViewEnquiry(request):
    tbl="";
    query="select * from tbl_contact";
    cur.execute(query);
    res=cur.fetchall();
    a=cur.rowcount;
    if(a>0):
        tbl+="<table class='table table-responsive' id='example'><thead><tr style='background:orangered;color:white'><th>Sn.</th><th>name</th><th>email</th><th>Mobile</th><th>Message</th><th>Delete</th><th>Update</th></tr></thead>";
        tbl+="<tbody>";
        for i in res:
            tbl+="<tr><td>"+str(i[0])+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td>"+str(i[3])+"</td><td>"+i[4]+"</td><td><a href='/AdminZone/Adelete?del="+str(i[0])+"'><span class='fa fa-trash'></span></a></td><td><a href='/AdminZone/Aupdate?up="+str(i[0])+"'><span class='fa fa-eye'></span></a></td></tr>";
        tbl+="</tbody>";
        tbl+="</table>";
    else:
        msg="No Record Found";
    return render(request,'AdminZone/ViewEnquiry.html',{'Tbl':tbl});
def Adelete(request):
    id=request.GET.get("del");
    query="delete from tbl_contact where Eid='"+id+"'";
    cur.execute(query);
    msg="Delete Data Successfully";
    return render(request,'AdminZone/Adelete.html',{'Msg':msg});

def Aupdate(request):
    msg="";name="";email="";mob="";message="";
    id=request.GET.get("up");
    query="select * from tbl_contact where eid='"+id+"'";
    cur.execute(query);
    res=cur.fetchall();
    a=cur.rowcount;
    if(a>0):
        name=res[0][1];email=res[0][2];mob=res[0][3];msg=res[0][4];
    if(request.method=="POST"):
        name=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        mob=request.POST.get("txtmob");
        msg=request.POST.get("txtmsg");
        query="update tbl_contact set name='"+name+"',email='"+email+"',mobile='"+mob+"',msg='"+msg+"' where eid='"+id+"'";
        cur.execute(query);
        message="Update Data Successfully";
    return render(request,'AdminZone/Aupdate.html',{'Name':name,'Email':email,'Mob':mob,'Msg':msg,'Message':message});
def ViewFeedback(request):
    id=request.session.get("aid");
    if(id!=None and id!=""):
       tbl ="";
       query ="select * from tbl_feedback";
       cur.execute(query);
       res = cur.fetchall();
       # a = cur.rowcount;
       # if (a > 0):
       tbl+= "<table class='table table-responsive' id='example'><thead><tr style='background:orangered;color:white'><th>fid</th><th>userid</th><th>rating</th><th>msg</th><th>fdt</th></tr></thead>";
       tbl+= "<tbody>";
       for i in res:
           tbl += "<tr><td>"+str(i[0])+"</td><td>"+i[1]+"</td><td>"+str(i[2])+"</td><td>"+i[3]+"</td><td>"+i[4]+"</td></tr>";
       tbl += "</tbody>";
       tbl += "</table>";
       # else:
       #     msg = "No Record Found";
    else:
        return redirect("/Login");
    return render(request,'AdminZone/ViewFeedback.html',{'Tbl':tbl});
def Changepassword(request):
    id = request.session.get("aid");
    if (id != None and id != ""):
       tbl="";
       query="select * from tbl_login";
       cur.execute(query);
       res=cur.fetchall();
       tbl +="<table class='table table-responsive' id='example'><thead><tr style='background:orangered;color:white'><th>userid</th><th>password</th><th>type</th><th>ldt</th></tr></thead>";
       tbl +="<tbody>";
       for i in res:
            tbl +="<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td>"+i[3]+"</td></tr>";
       tbl +="</tbody>";
       tbl +="</table>";
    else:
        return redirect("/Login");
    return render(request,'AdminZone/Changepassword.html',{'Tbl':tbl});
def alogout(request):
    id=request.session.get("aid");
    if (id!=None and id!=""):
        request.session.flush();
        request.session={};
        return redirect("/Login");
    else:
        return redirect("/Login");
    return render(request,'AdminZone/alogout.html');
@csrf_exempt
def AddNotification(request):
    id=request.session.get("aid");
    if(id!=None and id!=""):
        if(request.is_ajax()):
            name=request.POST.get("Name");
            msg=request.POST.get("Msg");
            query="insert into tbl_notification values('"+name+"','"+msg+"','"+str(dt)+"')";
            cur.execute(query);
            res="Notification Add successfully";
            return HttpResponse(res);
    else:
        return redirect("/Login");
    return render(request,'AdminZone/AddNotification.html');
def ViewNotification(request):
    tbl="";
    id=request.session.get("aid");
    if(id!=None and id!=""):
        query = "select * from tbl_notification";
        cur.execute(query)
        res=cur.fetchall();
        tbl+="<table class='table table-responsive' id='example'><thead><tr style='background:orangered;color:white'><th>name</th>" \
             "<th>message</th><th>ndt</th><th>Delete</th></tr></thead>";
        tbl+="<tbody>";
        for i in res:
            tbl+="<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td><a href='/AdminZone/ANdelete?del="+i[0]+"'><span class='fa fa-trash'></span></a></td></td></tr>";
        tbl+="</tbody>";
        tbl+="</table>";
    else:
        return redirect("/Login");
    return render(request,'AdminZone/ViewNotification.html',{'Tbl':tbl});
def ANdelete(request):
    message="";
    name=request.GET.get("del");
    query="delete from tbl_notification where nname='"+name+"'";
    cur.execute(query);
    message="delete data successfully";
    return render(request,'AdminZone/ANdelete.html',{'Message':message});
@csrf_exempt
def captcha(request):
    if(request.is_ajax()):
        ch1=str(random.randint(0,9));
        ch2=str(chr(random.randint(65,95)));
        ch3=str(chr(random.randint(97,122)));
        ch4=str(random.randint(5,8));
        ch5=str(random.randint(75,85));
        total=ch1+ch2+ch3+ch4+ch5;
        return HttpResponse(total);
    return render(request,'captcha.html');

