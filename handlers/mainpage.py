import os
import constants
import logging
import json

from google.appengine.ext.webapp import template

from authhandler import AuthHandler
from models.point import PointRoot, FeaturedPoint

class MainPage(AuthHandler):
    def getMainPageLeft(self):
        
        newPoints = PointRoot.getRecentCurrentPoints()
        featuredPoint = FeaturedPoint.getFeaturedPoint()
            
        vals = {
            'recentlyActive': newPoints,
            'featuredPoint': featuredPoint,
            'user': self.current_user
        }
        template = self.jinja2_env.get_template('mainPageLeftColumn.html')
        html = template.render(vals)

        resultJSON = json.dumps({
            'result': True,
            'html': html,
        }) 
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(resultJSON) 
        
    def getMainPageRight(self):      
        user = self.current_user

        if user:
            recentlyViewedPoints = user.getRecentlyViewed()
        else:
            recentlyViewedPoints = []
            
        vals = {
            'recentlyViewed': recentlyViewedPoints,
            'user': user
        }
        template = self.jinja2_env.get_template('mainPageRightColumn.html')        
        html = template.render(vals)
        

        resultJSON = json.dumps({
            'result': True,
            'html': html,
        }) 
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(resultJSON) 
    
    def get(self):

        newPoints = PointRoot.getRecentCurrentPoints()
        featuredPoint = FeaturedPoint.getFeaturedPoint()
        user = None

        if self.logged_in:
            user = self.current_user

        # GET RECENTLY VIEWED
        if user:
            recentlyViewedPoints = user.getRecentlyViewed()
            user.getActiveNotifications()
        else:
            recentlyViewedPoints = []
        template_values = {
            'recentlyActive': newPoints,
            'recentlyViewed': recentlyViewedPoints,
            'featuredPoint': featuredPoint,
            'user': user,
            'thresholds': constants.SCORETHRESHOLDS,
            'currentArea':self.session.get('currentArea')
        }
        template = self.jinja2_env.get_template('index.html')                
        self.response.out.write(template.render(template_values))
