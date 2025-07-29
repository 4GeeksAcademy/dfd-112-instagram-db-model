from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, String, Boolean, ForeignKey, Enum, CheckConstraint, PrimaryKeyConstraint, DateTime # "ForeignKey", "Enum", "CheckConstraint", "PrimaryKeyConstraint" imported
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime, timezone
import enum
# from enum import Enum
# from sqlalchemy.dialects.postgresql import ENUM as PGEnum
# from sqlalchemy.types import Enum as SQLAlchemyEnum


# Base = declarative_base() # ----> I cannot make this work

db = SQLAlchemy()
# class User(db.Model):

#########################################################################################
#########################################################################################
#############                            TABLES                             #############
#############                       with SQL Alchemy                        #############
#############                         and classes                           #############
#########################################################################################
#########################################################################################
"""
TO-DOs:

[x] Create tables for Instagram model:

    [x] User
    [x] Follower --> renamed as "Follow"
    [x] Comment
    [x] Post
    [x] Media

[x] Create MediaType (Enum) for using in Media.type
"""



############################################
###########         User         ###########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Atributes:
    [x] id
    [x] username
    [x] first_name
    [x] last_name
    [x] email

[x] Create Relations
    [x] with Follow, relating "user_from_id"
    [x] with Follow, relating "user_to_id"
    [x] with Comment
    [x] with Post

[x] Create serialization
"""
class User(db.Model):
    __tablename__ = "user"

    ### ATRIBUTES ###

    id:         Mapped[int]  = mapped_column(              primary_key=True)
    username:   Mapped[str]  = mapped_column( String(20),  unique=True,       nullable=False)
    first_name: Mapped[str]  = mapped_column( String(40),                     nullable=False)
    last_name:  Mapped[str]  = mapped_column( String(40),                     nullable=False)
    email:      Mapped[str]  = mapped_column( String(60),  unique=True,       nullable=False)
    password:   Mapped[str]  = mapped_column( String(40),                     nullable=False)
    is_active:  Mapped[bool] = mapped_column( Boolean(),   default=True,      nullable=False)


    ### RELATIONS ###

    # with Follow --> Users this user follows
    following: Mapped[list["Follow"]] = relationship(
        "Follow",
        foreign_keys="Follow.user_from_id",
        back_populates="follower"
        )
    
    # with Follow --> Users following this user
    followers: Mapped[list["Follow"]] = relationship(
        "Follow",
        foreign_keys="Follow.user_to_id",
        back_populates="followed"
        )
    
    # with Comment --> Comments made by this user
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="author"
        )

    # with Post --> Posts made by this user
    user_posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="post_author"
        )


    ### SERIALIZATION ###

    def serialize(self):
        return {
            "id":          self.id,
            "is_active":   self.is_active,
            "email":       self.email,
            "username":    self.username,
            "first_name":  self.first_name,
            "last_name":   self.last_name,
            "following":   [followed.serialize() for followed in self.following],
            "followers":   [follower.serialize() for follower in self.followers],
            "comments":    [comment.serialize()  for comment  in self.comments],
            "posts":       [post.serialize()     for post     in self.user_posts]
            # do not serialize the password, its a security breach !!!
        }



############################################
############       Follow       ############
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create composite PK with both ID's

[x] Create Atributes:
    [x] user_from_id
    [x] user_to_id
    [x] created_at

[x] Create Relations
    [x] with User -> from "user_from_id"
    [x] with User -> from "user_to_id"

[x] Create serialization
"""
class Follow(db.Model):
    __tablename__ = "follow"


    ### ATRIBUTES ###

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id:  Mapped[int]  = mapped_column(  ForeignKey("user.id"),   primary_key=True)
    user_to_id:    Mapped[int]  = mapped_column(  ForeignKey("user.id"),   primary_key=True)

    created_at:    Mapped[datetime] = mapped_column( DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))   # default=datetime.now

    ## COMPOSITE PRIMARY KEY
    __table_args__ = (
        PrimaryKeyConstraint("user_from_id", "user_to_id"),
        CheckConstraint("user_from_id != user_to_id", name="check_self_follow"),
    )


    ### RELATIONS ###
    
    # with User -> from "user_from_id" --> User who is following (follower)
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id],
        back_populates="following"
        )

    # with User -> from "user_to_id" --> User being followed (followed)
    followed: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="followers"
        )
    

    ### SERIALIZATION ###

    def serialize(self):   # IMPROVE THIS SERIALIZATION
        return {
            "user_from_id":  self.user_from_id,
            "user_to_id":    self.user_to_id,
            "created_at":    self.created_at.isoformat() if self.created_at else None
        }



############################################
###########        Comment       ###########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Atributes:
    [x] id
    [x] comment_text
    [x] author_id
    [x] post_id
    [x] created_at

[x] Create Relations
    [x] with User
    [x] with Post

[x] Create serialization
"""
class Comment(db.Model):
    __tablename__ = "comment"

    ### ATRIBUTES ###

    id:           Mapped[int]     = mapped_column(               primary_key=True)
    comment_text: Mapped[str]     = mapped_column( String(500),                         nullable=False)
    author_id:    Mapped[int]     = mapped_column(               ForeignKey("user.id"))
    post_id:      Mapped[int]     = mapped_column(               ForeignKey("post.id"))

    created_at:  Mapped[datetime] = mapped_column( DateTime(timezone=True),   default=lambda: datetime.now(timezone.utc))   # default=datetime.now


    ### RELATIONS ###

    # with User --> User who wrote the comment
    author: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
        )

    # with Post --> Post this comment belongs to
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
        )


    ### SERIALIZATION ###
    
    def serialize(self):
        return {
            "id":            self.id,
            "comment_text":  self.comment_text,
            "author_id":     self.author_id,
            "post_id":       self.post_id,
            "created_at":    self.created_at.isoformat() if self.created_at else None
        }


############################################
###########         Post         ###########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Atributes:
    [x] id
    [x] user_id
    [x] created_at

[x] Create Relations
    [x] with User
    [x] with Comment
    [x] with Media

[x] Create serialization
"""
class Post(db.Model):
    __tablename__ = "post"

    ### ATRIBUTES ###

    id:        Mapped[int]  = mapped_column(  primary_key=True)
    user_id:   Mapped[int]  = mapped_column(  ForeignKey("user.id"),   nullable=False)

    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True),   default=lambda: datetime.now(timezone.utc))   # default=datetime.now

    ### RELATIONS ###

    # with User --> User who created the post
    post_author: Mapped["User"] = relationship(
        "User",
        back_populates="user_posts"
        )

    # with Comment --> Comments on this post
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post"
        )

    # with Media --> Media attached to this post
    media: Mapped[list["Media"]] = relationship(
        "Media",
        back_populates="post"
        )


    ### SERIALIZATION ###

    def serialize(self):
        return {
            "id":          self.id,
            "user_id":     self.user_id,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
            "media":       [media.serialize()   for media   in self.media],
            "comments":    [comment.serialize() for comment in self.comments]
        }


############################################
###########         Media        ###########
############################################
"""
TO-DO's:

[x] Create "MediaType" class for Enum data type

[x] Name the table with "__tablename__ ="

[x] Create Atributes:
    [x] id
    [x] type -----------------------------------> COULD NOT MAKE IT WORK WITH ENUM TYPE, changed to a string
    [x] url
    [x] post_id

[x] Create Relations
    [x] with Post

[x] Create serialization
"""
############################################################
"""
With the type "mediatype" with enum (enumeration) it gives an error, I don't know how to fix it, I am removing it so that the error doesn't appear when creating the "diagram.png"
"""
### Media type for the "enum" data type
# class MediaType(enum.Enum):
#     IMAGE   = "image"
#     VIDEO   = "video"
#     PENDING = "pending"

############################################################
class Media(db.Model):
    __tablename__ = "media"

    ### ATRIBUTES ###

    id:       Mapped[int]        = mapped_column(                   primary_key=True)
    # type:     Mapped[MediaType]  = mapped_column( Enum(MediaType),                                        nullable=False)  ### -------------------------->  OUTPUTS ERROR WHEN CREATING TABLE
    # type:     Mapped[MediaType]  = mapped_column( PGEnum(MediaType, name="mediatype", create_type=True),  nullable=False)  ### -------------------------->  OUTPUTS ERROR WHEN CREATING TABLE
    # type:     Mapped[MediaType]  = mapped_column( SQLAlchemyEnum(MediaType, name="media_type"), default=MediaType.PENDING,  nullable=False) ### --------->  OUTPUTS ERROR WHEN CREATING TABLE
    type:     Mapped[str]        = mapped_column(  String(40),                                            nullable=False)
    url:      Mapped[str]        = mapped_column(  String(255),                                           nullable=False)
    post_id:  Mapped[int]        = mapped_column(                   ForeignKey("post.id"),                nullable=False)


    ### RELATIONS ###

    # with Post --> Post this media belongs to
    post: Mapped["Post"] = relationship(
        "Post",
          back_populates="media"
          )


    ### SERIALIZATION ###

    def serialize(self):
        return {
            "id":       self.id,
            "type":     self.type,
            "url":      self.url,
            "post_id":  self.post_id,
        }




