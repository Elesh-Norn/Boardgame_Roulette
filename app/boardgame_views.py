from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from marshmallow import ValidationError
from app import app, db
from app.models import User, Post, Boardgame
from app.forms import AddBoardgame, RandomGame
from app.schema import SearchSchema


@app.route("/collection", methods=["GET", "POST"])
@login_required
def collection():
    form = AddBoardgame()
    if form.validate_on_submit():
        game = Boardgame(
            title=form.title.data,
            player_number_min=form.player_number_min.data,
            player_number_max=form.player_number_max.data,
            playtime_low=form.playtime_low.data,
            playtime_max=form.playtime_max.data,
        )

        if current_user.own_game(game):
            flash("You already have this game")
            return redirect(url_for("collection"))

        isgameindb = Boardgame.query.filter_by(title=game.title).first()
        if not isgameindb:
            db.session.add(game)

        current_user.add_game(game)
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("collection"))
    games = current_user.collection
    return render_template(
        "collection.html", title="Your collection", games=games, form=form
    )


@app.route("/random", methods=["GET", "POST"])
@login_required
def random():
    form = RandomGame()
    game = None
    if request.method == "POST":
        schema = SearchSchema()
        try:
            result = schema.load(form.data)
        except ValidationError as err:
            result = err.valid_data
        if not result:
            flash("You didn't fill any fields")
            return redirect(url_for("random"))
        game = current_user.random_game(result)
        if game is None:
            flash("You do not posses games that match those criteria")
            return redirect(url_for("random"))
        else:
            flash("You can play {}".format(game))
            return redirect(url_for("random"))
    return render_template("random.html", game=game, form=form)
