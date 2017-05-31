from google.appengine.ext import ndb


class Post(ndb.Model):
    """ Blog Post data model for datastore """
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    posting_user = ndb.StringProperty(required=True)

    def render(self):
        """ escape all html tags from post, then convert newlines to <br> """
        escaped_post = jinja2.escape(self.content)
        self._render_text = escaped_post.replace('\n', jinja2.Markup('<br>'))
        return render_str("post.html", p=self)

    def peek(self):
        """ Show first part of long posts to not overload multi-post pages """
        escaped_post = jinja2.escape(self.content)
        marked_up_post = escaped_post.replace('\n', jinja2.Markup('<br>'))
        if len(marked_up_post) > 1000:
            self._render_text = marked_up_post[:1000]
            return render_str("previewpost.html", p=self)
        else:
            self._render_text = marked_up_post
            return render_str("post.html", p=self)


class Comment(ndb.Model):
    """ Comments data model used for datastore """
    comment_text = ndb.TextProperty(required=True)
    parent_post_id = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    posting_user = ndb.StringProperty(required=True)

    def render(self):
        """ Draws comments """
        escapedcomment = jinja2.escape(self.comment_text)
        marked_up_comment = escapedcomment.replace('\n', jinja2.Markup('<br>'))
        self._render_text = marked_up_comment
        return render_str("comment.html", c=self)


class Secret(ndb.Model):
    """ HMAC Secret Key stored in datastore. Used to verify session cookies """
    key_string = ndb.StringProperty(required=True)


class User(ndb.Model):
    """ User account info for auth """
    username = ndb.StringProperty(required=True)
    user_hash = ndb.StringProperty(required=True)
    salt = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    current_session = ndb.StringProperty(required=False)
    session_expires = ndb.DateTimeProperty(required=False)


class AntiCsrfToken(ndb.Model):
    """ Anti forgery token embedded in hidden form fields used
        to ensure the request came from the site and not an external site """
    csrf_sync_token = ndb.StringProperty(required=True)
    associated_user = ndb.StringProperty(required=True)


class ResetToken(ndb.Model):
    """ Password reset token used in email when user forgot their password """
    associated_acct_email = ndb.StringProperty(required=True)
    token_guid = ndb.StringProperty(required=True)
    expires = ndb.DateTimeProperty(required=True)


class LoginAttempt(ndb.Model):
    """ Keeps track of login attempts for rate limiting """
    ip_addr = ndb.StringProperty(required=True)
    last_attempt = ndb.DateTimeProperty(required=True)
    attempt_count = ndb.IntegerProperty(required=True)