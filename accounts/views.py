from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)
from .forms import UserLoginForm, UserRegisterForm

