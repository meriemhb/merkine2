from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

def article_list(request):
    """Vue pour lister les articles"""
    articles = Article.objects.filter(published=True)
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, slug):
    """Vue pour afficher les détails d'un article"""
    article = get_object_or_404(Article, slug=slug, published=True)
    comments = article.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

@login_required
def article_create(request):
    """Vue pour créer un article"""
    if request.user.user_type != 'kine':
        messages.error(request, 'Seuls les kinésithérapeutes peuvent créer des articles.')
        return redirect('blog:article_list')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_update(request, pk):
    """Vue pour modifier un article"""
    article = get_object_or_404(Article, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    """Vue pour supprimer un article"""
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cet article.')
        return redirect('blog:article_detail', slug=article.slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'L\'article a été supprimé avec succès.')
        return redirect('blog:article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})

@login_required
def add_comment(request, pk):
    """Vue pour ajouter un commentaire"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        # Logique d'ajout de commentaire
        pass
    return redirect('blog:article_detail', slug=article.slug) 