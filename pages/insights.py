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
        
            ## Insights
            ### What stats does my model think are important?

            After I finished making new stats--see my "Process" page for details--I ended up with over 100 stats to plug
            into my model. But, as you might expect, some ended up being more important than others.

            I used a [function](https://eli5.readthedocs.io/en/latest/blackbox/permutation_importance.html) from the library eli5
            called "Permutation Importance." The basic idea is to randomly shuffle around the data in turn for each stat,
            and the more that shuffling makes the prediction works, the more important that stat is. You can find the result
            of this calculation in the table to the right.

            Despite the accuracy of the baseline estimate--that each player will log as many assists this season as the previous
            one--you can see that assist rate is only the 4th-most important stat! The other three are all stats that I created:
            points and assists adjusted (i.e. multiplied by) minutes played, and the player's average career assist rate. A
            fourth stat I created, the average (adjusted) points per game of all the player's teammates last season, came
            in fifth.

            What patterns can we see here? The fact that so many places are taken up by my adjusted stats indicates that
            the base "number of X per game" stat is insufficient; it's more important to know if the player maximized
            his value in the minutes he got. The prevalence of the points stat, on the other hand, is somewhat surprising
            to me; you'd think the more points a player scores, the *less* he'd want to pass the ball, but the truth--
            as I'll also demonstrate shortly--appears to be the opposite. Perhaps happy people are more likely
            to want to help others as well?

            ### Graphing correlations

            The permutation importances above can be further corroborated, if not necessarily confirmed, by graphing each of the
            four most important stats against our target--i.e., next season's assist rate. While some correlations are more obvious
            than others, they all have a relatively strong positive correlation. In other words, the more adjusted points
            and (adjusted/career) assists a player had in a given year, the more assists per game they had the following year.
            Of course we all know that correlation doesn't prove causation. But combined with the permutation importances
            above, I think they tell a fairly convincing case.


            """
        ),
    ],
    md=4,
)


column2 = dbc.Col(
    [
        html.Img(src='assets/perm-importances.PNG', className='img-fluid'),
        html.Img(src='assets/pts-adj-vs-target.png', className='img-fluid'),
        html.Img(src='assets/ast-adj-vs-target.png', className='img-fluid'),
        html.Img(src='assets/cas-vs-target.png', className='img-fluid'),
        html.Img(src='assets/ast-vs-target.png', className='img-fluid')
    ]
)

row1 = dbc.Row([column1, column2])

row2 = dbc.Row(
    [dcc.Markdown(
        """

        ### Individual predictions

        Finally, we can also use those permutation importances to help us see the impact each stat has on a player's
        predicted assist rate. (It would be very difficult to understand a 100-part graph!) Below you can see three
        such graphs. Each one starts at the same value, but depending on the player's stats, they end up traveling very
        different paths.

        Jeff Teague, for example, is a player my model and the baseline heavily disagreed upon. In the 2017-2018 season,
        he completed an impressive 7 assists a game for the Minnesota Timberwolves. My model guessed he would decline to
        a rate of a little over 6 per game; but beating expectations, he managed 8.2 (!) assists per game in the
        2018-2019 season.

        Other times, both my model and the baseline get a player very wrong. In the 2017-2018 season, Sacramento Kings
        point guard De'Aaron Fox only made 4.4 assists per game; not so impressive, given his position. My model thought
        he would stay about the same in the next season, but instead he skyrocketed up to 7.3.

        But of course, some players are just boring. (Former) Boston Celtic Terry Rozier made 2.9 assists per game in
        2017-18, my model predicted he'd stay the same for 2018-19, and that's exactly what he did, making 2.9
        assists yet again. Consistency is often a virtue--but in this case, perhaps not.

        Naturally, sometimes, my model does beat the baseline. See John Wall for instance, who made 9.6 assists per game
        in 2017-18, but in the following year regressed to 8.7, almost exactly as my model predicted. (Sadly, he also
        suffered a series of devastating injuries that season.) Unfortunately, his graph reveals a weakness of my method
        of calculating the impact of stats on result; whether it's because I'm excluding too many stats, or not taking
        into account an important aspect of Ridge Regression, Wall's prediction on the chart is different from the
        actual prediction in my model. There's always a tradeoff, I suppose.


        """
    )]
)

row3 = dbc.Row(
    [
        html.Img(src='assets/teague-prediction.png', className='img-fluid'),
        html.Img(src='assets/fox-prediction.png', className='img-fluid'),
        html.Img(src='assets/rozier-prediction.png', className='img-fluid'),
        html.Img(src='assets/wall-prediction.png', className='img-fluid')
    ]
)

column3 = dbc.Col(
    [dcc.Markdown(
        """

        ### Conclusion

        So what can we conclude? Does the importance of points per game mean that, as I suggested earlier, happy people
        help people? Does team points in 5th place mean that people are willing to be selfless, as long as people
        make effective use of the aid they receive? Of course, assists aren't necessarily "selfless"; there are plenty of
        players who try to make themselves look better by padding their assist stat, dating all the way back to (at least)
        the great Wilt Chamberlain.

        This situation appears to call out for a weak-willed "I guess we may never know" sort of conclusion. But if there
        is one lesson we can draw from my model, I think it's that we shouldn't just look at raw stats. A simple adjustmnet
        of multiplying by minutes played created a great deal of useful stats; who knows what other truths are lying
        in those numbers?

        """
    )]
)

column4 = dbc.Col(
    [html.Img(src='assets/durant.jpg', className='img-fluid')]
)

row4 = dbc.Row([column3, column4])

layout = dbc.Col([row1, row2, row3, row4])