from django.views import generic
from .models import Post ,Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render , HttpResponse,redirect
from django.contrib.auth.decorators import login_required

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

# def PostDetail(request,slug):
#     model = Post 
#     template_name = 'post_detail.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add comments related to this post to the context
        post = self.get_object()
        # print(post.slug)
        comments = Comment.objects.filter(post=post.slug, approved_comment=True)
        
        context['comments'] = comments

        return context

def auth_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    
    user = authenticate(request, username=username, password=password)
    if user is not None:

        login(request, user)

        return redirect("/")
        # Redirect to a success page.
        ...
    else:
        return redirect("/")
    
def authlogout(request):
    logout(request)
    return redirect("/")

def signup(request):
    fname= request.POST["fname"]
    lname= request.POST["lname"]
    email= request.POST["email"]
    username= request.POST["username"]
    password= request.POST["password"]
    User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password).save()
    return redirect("/")
@login_required(login_url='/')    
def postblog(request):
    yourblog=Post.objects.filter(author=request.user)


    return render(request,"postblog.html",{"blog":yourblog})

@login_required(login_url='/')    
def blogsubmit(request):
    print(request.user.id)
    title= request.POST["title"]
    blog= request.POST["blog"]
    if "status" in request.POST:
        status= 1
    else:
        status= 0
    print(status)
    Post(title=title,content=blog,status=status,author=request.user).save()
    return redirect("/postblog")

# from django.shortcuts import render, redirect
# from .models import Comment  # Import your Comment model
# from .forms import CommentForm  # Import a CommentForm if you have one

def submit_comment(request):
    if request.method == "POST":
        post_slug= request.POST["slug"]
        comment= request.POST["comment"]
        Comment(post=post_slug,author=request.user,text=comment).save()


    # Assuming you have a CommentForm defined to handle comment submissions

            # You can also add a message to indicate the comment was added successfully
            # messages.success(request, 'Your comment has been added successfully.')

    # Redirect back to the post detail page where the comment was submitted
    return redirect(f"/{post_slug}")  # Replace 'post_detail' with your actual view name
