from create_sql import db,user,Follow
class current_user():
    def _init__(self,id,):
        self.id = id
    def follow(self,user):
        if not self.is_following(user):
            fo = Follow(follower_id=self.id,followed_id=user.id)
            db.session.add(fo)
            db.session.commit()
    def unfollow(self,user):
        if self.is_following(user):
            fo = self.followed.filter_by(followed_id=user.id)
            db.session.delete(fo)
            db.session.commit()
    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first()
    def is_followed_by(self,user):
        return self.follower.filter_by(follower_id=user.id).first()