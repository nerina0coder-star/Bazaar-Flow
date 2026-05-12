from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit

from app.extensions import db
from app.models.message import Message