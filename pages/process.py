import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process

            ### Why NBA assists?

            I started following the NBA just last year, but I'm already addicted--though I admit that
            the storylines *around* the games are often more fun than the games themselves.
            In addition to my interest, there's a wealth of data about the NBA on the website
            [Basketball Reference][basketball-reference.com], which made it relatively
            straightforward to gather the data I needed for making predictions (more on that
            in a bit.) I was also curious--perhaps predicting assists might teach us some things,
            not only about basketball, but even about selfishness and altriusm.

            There were three main steps to getting the data necessary for this project: gather
            the data, manipulate it into a usable form, then construct and test models.

            """
        ),

    ],
)

column2 = dbc.Col(
    [html.Img(src='assets/picture1.jpg', className='img-fluid')]
)

row1 = dbc.Row([column1, column2])

column3 = dbc.Col(
    [html.Img(src='assets/picture2.jpg', className='img-fluid')]
)

column4 = dbc.Col(
    [dcc.Markdown(
        """

        ### Gathering data

        I collected all of my data from Basketball Reference. While this made things straightforward,
        especially since Basketball Reference names their pages in a logical way, there
        were still some difficulties.

        Collecting the player data was the easiest part; Basketball Reference has a separate stats page
        for each season (for instance,
        [here's the 2018-2019 season](https://www.basketball-reference.com/leagues/NBA_2019_per_game.html)),
        and to get data for other seasons you just have to change the year in the URL. There is a minor
        complication since there are two now-defunct leagues, the BAA and the ABA, that I also wanted
        data for, but that was just a matter of changing "NBA" in the title.

        I also wanted data on each team's roster per year, though, and that was a bit harder. Basketball
        Reference does have that data (e.g. [here](https://www.basketball-reference.com/teams/LAC/2020.html)),
        but as you can see if you click that link, the team name is in the URL. The problem is that, when
        I scrape the data, I need to make sure I don't try to scrape data from a page that doesn't exist!
        Luckily, I could use the data I gathered on players' season stats to determine which basketball
        teams existed in which years, since those stats also included the team that player played for.

        Finally, I wanted data on all-star appearances; basically an award the NBA gives to its best players.
        This was especially difficult since Basketball Reference [stores that data](https://www.basketball-reference.com/leagues/NBA_2019.html#all_all_star_game_rosters)
        in a form that's much harder to get to than the tables in the previous pages. But, with help
        from a colleague, I was able to do it in the end.

        (For more details, see [this Python notebook.](https://github.com/davidanagy/nba-assists-prediction/blob/master/notebooks/Obtaining_Data.ipynb))

        I would like to thank Luis Felipe Bueno for his [very helpful guide](https://lfbueno.com/2019-02-19-scrape-bb/)
        and my colleague Richmond Macaspac; without them, this step would've been a lot harder.

        """
    )]
)

row2 = dbc.Row([column3, column4])

column5 = dbc.Col(
    [dcc.Markdown(
        """

        ### Wrangling Data

        By "wrangling," I mean both (a) cleaning the data to make it usable and (b) making new features--i.e., constructing
        new stats--to help my model.

        There were a lot of missing values in my data, and for separate reasons too--in some cases, because the data
        just doesn't exist (mostly for old seasons), but others had more specific reasons. For instance, the "3-point percentage" (3P%)
        stat is calculated by dividing 3-point shots made (3P) by 3-point shots attempted (3PA). But if the player didn't attempt
        a single 3-point shot the entire season--which happens more often than you might think, even for people not named
        [Ben Simmons](https://www.espn.com/nba/story/_/id/27897301/ben-simmons-here-your-3-point-shooting-revolution)--then their "3PA"
        stat equals 0. And since you can't divide by zero, the result is a missing value. For those percentage stats, I just filled
        the missing values with zeroes; for others, I put in the median value across the whole dataset. The most interesting case
        was "games started" (GS); I figured I could rather accurately estimate that through the other stats, particularly minutes
        played (MP), since the better players are more likely both to start and to play heavy minutes. So for that stat alone,
        I made a model to predict the missing values.

        Making new features was a whole different beast. Some ideas I had were easy to implement. The most important was to add
        a "Target" stat--this is just the value my model is trying to predict. Since I'm trying to predict players' assist rates
        *next* season, I just made the "Target" stat, for each year, the Assist stat of the *following* year. (NBA stat heads
        might ask, why am I using per game numbers? While I do think per-minute or per-possession numbers more accurately
        capture a player's worth, the per-game numbers are more familiar, and this project isn't really about determining
        whether a player is good or bad anyway.) Additionally I had an idea to adjust each player's stats by their minutes played--
        I just multiplied each stat by "Minutes Played," and got new "adjusted" stats for all of them.

        More complicated was determining what I call their *team* stats. I thought that maybe a player would be more likely to pass if
        e.g. his teammates have a higher shooting percentage, or just score more points in general. So I wanted to create stats that
        averaged each teammate's stats for the previous season. This proved more difficult than might be expected; the straightforward,
        brute-force solution would've taken my computer over four days to complete! But by carefully manipulating my teams dataset,
        I was able to combine my data together in such a way that I got those stats in a much shorter amount of time. Similarly,
        by sorting my all-star data correctly, I was able to (somewhat) easily acquire information about how many all-star teams
        a player had made in each year of their professional career.

        (For more detail, see [this Python notebook.](https://github.com/davidanagy/nba-assists-prediction/blob/master/notebooks/Wrangling_Data.ipynb))

        """
    )]
)

column6 = dbc.Col(
    [html.Img(src='assets/picture3.jpg', className='img-fluid')]
)

row3 = dbc.Row([column5, column6])

column7 = dbc.Col(
    [html.Img(src='assets/picture4.jpg', className='img-fluid')]
)

column8 = dbc.Col(
    [dcc.Markdown(
        """

        ### Making Models

        To be honest, this might've been the easiest part of the whole process, even though it's the purpose of the entire enterprise.
        Once I got my data nice and wrangled, it was just a matter of testing various models--and various variations of models--on it,
        until I saw which one did the best.

        One important thing to note is that I essentially did a "four-way split" of my data. Since my main goal is to predict assists
        in the 2019-2020 season, I decided to make the 2018-2019 season my "test set"; in other words, I held it out until the end,
        to make sure it didn't unduly bias my models. I then made every season from 2013-14 until 2016-17 my "validation" set,
        using it over and over to try to determine the best ways to tune my models.

        In the end, it turned out that a [Ridge Regression](https://www.statisticshowto.datasciencecentral.com/ridge-regression/) was
        the best-performing model. However, compared to the baseline prediction of just assuming each player will have the same
        number of assists as the previous year, my model only represented a little over a 9 percent improvement (using [mean
        squared error](https://en.wikipedia.org/wiki/Mean_squared_error) as my metric). But since the baseline is quite accurate,
        and assist numbers are relatively now, perhaps this isn't too surprising. Though of course, the real test of my model
        will be how it does in predicting the upcoming season!

        (For more detail, see [this Python notebook.](https://github.com/davidanagy/nba-assists-prediction/blob/master/notebooks/Modeling.ipynb))

        """
    )]
)

row4 = dbc.Row([column7, column8])

column9 = dbc.Col(
    [dcc.Markdown(
        """

        ### Conclusion

        Even though my model isn't a huge improvement on the baseline, I think it still provides some interesting information. If
        you'd like to know more, check out my Insights page--or try creating your own player and seeing how generous
        I think he'd be with the ball!

        Please feel free to email or DM me if you have any comments or questions.

        """
    )]
)

column10 = dbc.Col(
    [html.Img(src='assets/picture5.jpg', className='img-fluid')]
)

row5 = dbc.Row([column9, column10])

layout = dbc.Col([row1, row2, row3, row4, row5])