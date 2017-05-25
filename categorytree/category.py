#!/usr/bin/env python3
import sqlite3
import os
import sys

DATABASE = 'category.db'

def get_connection():
    return sqlite3.connect(DATABASE)

class Category:
    """Exposes methods for getting a category from local database."""

    def get(self,id):
        """Return category for the given id."""
        category = None        
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM category WHERE id = " +  str(id))
            category = c.fetchone()
        return category

    def get_direct_children(self,id):
        """Returns the children categories for the given id."""    
        with get_connection() as conn:
            c = conn.cursor()
            categories = None
            #We can have one more index for name.Just a point
            c.execute("SELECT * FROM category WHERE parent_id = " +  str(id) +" order by name")
            categories = c.fetchall()
        return categories        

    def sub_tree_for_category(self,id):
        """Create a html file with the subtree rooted at given id."""
        if not os.path.exists(DATABASE):
            sys.exit("No Category Repository Found")
        category = self.get(id)        
        if not category:
            sys.exit("No category with ID: "+str(id))
        body = '<ul>'+self.build(category)+'</ul'
        with open('templates/header.txt', 'r') as f:
            header=f.read()
        with open('templates/footer.txt', 'r') as f:
            footer=f.read()
        full_tree = header+body+footer
        html_file= open(str(id)+'.html',"w")
        html_file.write(full_tree)
        html_file.close()

    def build(self,category):
        """Build the tree recursively."""
        sub_tree = '<li>'+str(category[0])+':'+category[1]+':'+str(category[2])+':'+str(1 == category[3])
        child_categories = self.get_direct_children(category[0])        
        sub_sub_tree = ''
        if child_categories:
            for category in child_categories:
                child_tree = self.build(category)        
                sub_sub_tree = sub_sub_tree + child_tree
        sub_tree = sub_tree+'<ul>'+sub_sub_tree+'</ul>'+'</li>'
        return sub_tree

