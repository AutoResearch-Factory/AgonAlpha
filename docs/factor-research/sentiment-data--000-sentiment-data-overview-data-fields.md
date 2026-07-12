# Sentiment Data Overview & Data Fields

Course: Sentiment Data
Category: Data
Duration: PT6M54S
Source: VidYard
Last modified: 2023-04-28T11:39:09.214037-04:00

## Description

This video explains how sentiment data, which is often found on social media, can help better predict market behavior by identifying the mood surrounding a stock.
Out of the 12 data fields discussed in the video: the bearish, bullish and ratio data fields are no longer on the platform. The Python expression is not supported. Instead, you can simulate rank(snt_social_value)

## Transcript

In this video
we will discuss the sentiment dataset
and some of the data fields
supported.
We will also talk about
how to use these datasets in
the expression and the Python framework.
First, let's talk about
sentiment data.
Sentiment represents the aggregate
pulse or collective market
mood about the stock.
A rising stock price is
associated with positive
or bullish sentiment.
Along the same lines, a falling
stock price is characterized
by a negative or bearish sentiment.
The two types of sentiments
combine to produce the
overall mood surrounding a stock.
Intensity of sentiment represents
the strength of the sentiment.
A high intensity of sentiment
regardless of the mood, or
direction of the sentiment exists
when strong market moves
occur. For example,
positive market sentiment combined
with high intensity is typically
a characteristic of strong bullish
moves in prices. With
the rise of social media, many
discussions, posts and predictions
about future stock price movements
are available. This activity is captured
in the social media sentiment value
data field. One of the market's
characteristics is that generally
not all investors have a strong
bullish or bearish perspective.
Some people can be mildly bullish
or bearish. Some can have
strong bullish or bearish sentiment
and some can have opposite sentiments
or expectations about the market.
We can measure bullish
or bearish sentiment values individually
on a common scale - for example,
between 0 to 4. Sentiment
data can help us better predict market
behavior
and improve our forecasting,
not only for price direction but
also volatility and
volume traded. Now let's discuss
the data fields of sentiment data
supported by websim and
see what information they captured.
The first data field is this sentiment
value which represents
the mood of the overall sentiment.
A value greater than zero
represents an overall bullish
sentiment
and a negative value represents
an overall bearish sentiment.
The next data field is sentiment buzz,
which represents the intensity
or strength of the sentiment.
A value greater than one represents
high intensity and a value lower
than one represents low intensity.
The next data field we have is
the sentiment buzz backfilled
which is equivalent to
the sentiment buzz data
with the difference that an average value
of one is replaced
when the data entry is missing.
Sentiment buzz returns is
the percentage change in
sentiment buzz value from
the previous day.
It is similar to price returns but
here we use sentiment buzz values
to calculate the returns. Bearish
sentiment is measure of bearish
sentiment on a scale of 0
to 4. Bullish sentiment
is the measure of bullish sentiment
on a scale of 0 to 4.
The next data field which is a sentiment
ratio is the ratio that assesses
the overall sentiment of the market.
Using the ratio of bullish
to bearish sentiment values.
This data value is created
from the raw values and is
different from the ratio of sentiment
bullish and sentiment bearish
data field. Sentiment ratio
time series rank represents
the time series rank of
the sentiment ratio data.
Bearish sentiment time series
rank represents the time series
rank of the various sentiment
data field.
Bullish sentiment time series rank
represents the time series rank of
the bullish sentiment data field.
Social sentiment value
indicates the normalized value
of sentiment derived from
the information on social media.
Social sentiment volume
indicates the amount of activity observed
on social media.
We use this to derive the sentiment
of the discussions. Higher volumes
indicate more activity.
Now I will show you how to use
one of the data fields in the Python
framework. The expression
equivalent of the Python code
would be as on your screen.
We import the sentiment social
value in the variable
'social_snt_value'.
'dr' represents the data registry
from which we retrieve the data.
We then create a function called generate
which has two input arguments:
di
and Alpha.
Di represents the date index
and Alpha is the vector we
used to store the weights of
the different stocks in the universe for
a given day of a simulation.
The variable k is the date
index adjusted for the delay
we used in the simulation settings.
We assigned the rank of social
sentiment value variable to the
Alpha vector.
The rank operator is already
implemented in the Python framework
and is imported from the WebSim
Python library.
And finally we use the mask
factor
to store the entries of the valid
matrix for today’s delay-adjusted
date index k.
The valid matrix is a 2D
Boolean matrix, which tells
you if a given stock is present
in the selected universe for
different dates.
We set the stocks marked
false in the mask vector
to NaN;
this ensures we are trading the stocks
of only the selected universe.
To summarize,
sentiment data provides good
information about intensity
and direction of the sentiment
of a stock in the market.
This information can be used
in different Alphas in many different
ways.
