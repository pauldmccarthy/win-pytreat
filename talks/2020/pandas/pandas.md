# Pandas

Follow along online at: https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020/-/blob/master/talks/pandas/pandas.ipynb

Pandas is a data analysis library focused on the cleaning and exploration of
tabular data.

Some useful links are:
- [main website](https://pandas.pydata.org)
- [documentation](http://pandas.pydata.org/pandas-docs/stable/)<sup>1</sup>
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)<sup>1</sup> by
  Jake van der Plas
- [List of Pandas tutorials](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html)

<sup>1</sup> This tutorial borrows heavily from the pandas documentation and
the Python Data Science Handbook

```
%pylab inline
import pandas as pd  # pd is the usual abbreviation for pandas
import matplotlib.pyplot as plt # matplotlib for plotting
import seaborn as sns  # seaborn is the main plotting library for Pandas
import statsmodels.api as sm  # statsmodels fits linear models to pandas data
import statsmodels.formula.api as smf
from IPython.display import Image
sns.set()  # use the prettier seaborn plotting settings rather than the default matplotlib one
```

> We will mostly be using `seaborn` instead of `matplotlib` for
> visualisation. But `seaborn` is actually an extension to `matplotlib`, so we
> are still using the latter under the hood.

## Loading in data

Pandas supports a wide range of I/O tools to load from text files, binary files,
and SQL databases. You can find a table with all formats
[here](http://pandas.pydata.org/pandas-docs/stable/io.html).

```
titanic = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv')
titanic
```

This loads the data into a
[`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
object, which is the main object we will be interacting with in pandas. It
represents a table of data.  The other file formats all start with
`pd.read_{format}`.  Note that we can provide the URL to the dataset, rather
than download it beforehand.

We can write out the dataset using `dataframe.to_{format}(<filename>)`:

```
titanic.to_csv('titanic_copy.csv', index=False)  # we set index to False to prevent pandas from storing the row names
```

If you can not connect to the internet, you can run the command below to load
this locally stored titanic dataset

```
titanic = pd.read_csv('titanic.csv')
titanic
```

Note that the titanic dataset was also available to us as one of the standard
datasets included with seaborn. We could load it from there using

```
sns.load_dataset('titanic')
```

`Dataframes` can also be created from other python objects, using
`pd.DataFrame.from_{other type}`. The most useful of these is `from_dict`,
which converts a mapping of the columns to a pandas `DataFrame` (i.e., table).

```
pd.DataFrame.from_dict({
    'random numbers': np.random.rand(5),
    'sequence (int)': np.arange(5),
    'sequence (float)': np.linspace(0, 5, 5),
    'letters': list('abcde'),
    'constant_value': 'same_value'
})
```

For many applications (e.g., ICA, machine learning input) you might want to
extract your data as a numpy array. The underlying numpy array can be accessed
using the `to_numpy` method

```
titanic.to_numpy()
```

Note that the type of the returned array is the most common type (in this case
object). If you just want the numeric parts of the table you can use
`select_dtypes`, which selects specific columns based on their dtype:

```
titanic.select_dtypes(include=np.number).to_numpy()
```

Note that the numpy array has no information on the column names or row indices.
Alternatively, when you want to include the categorical variables in your later
analysis (e.g., for machine learning), you can extract dummy variables using:

```
pd.get_dummies(titanic)
```

## Accessing parts of the data

[Documentation on indexing](http://pandas.pydata.org/pandas-docs/stable/indexing.html)

### Selecting columns by name

Single columns can be selected using the normal python indexing:

```
titanic['embark_town']
```

If the column names are simple strings (not required) we can also access it
directly as an attribute

```
titanic.embark_town
```

Note that this returns a pandas
[`Series`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html)
rather than a `DataFrame` object. A `Series` is simply a 1-dimensional array
representing a single column.  Multiple columns can be returned by providing a
list of columns names. This will return a `DataFrame`:

```
titanic[['class', 'alive']]
```

Note that you have to provide a list here (square brackets). If you provide a
tuple (round brackets) pandas will think you are trying to access a single
column that has that tuple as a name:

```
titanic[('class', 'alive')]
```

In this case there is no column called `('class', 'alive')` leading to an
error.  Later on we will see some uses to having columns named like this.

### Indexing rows by name or integer

Individual rows can be accessed based on their name (i.e., the index) or integer
(i.e., which row it is in). In our current table this will give the same
results. To ensure that these are different, let's sort our titanic dataset
based on the passenger fare:

```
titanic_sorted = titanic.sort_values('fare')
titanic_sorted
```

Note that the re-sorting did not change the values in the index (i.e., left-most
column).

We can select the first row of this newly sorted table using `iloc`

```
titanic_sorted.iloc[0]
```

We can select the row with the index 0 using

```
titanic_sorted.loc[0]
```

Note that this gives the same passenger as the first row of the initial table
before sorting

```
titanic.iloc[0]
```

Another common way to access the first or last N rows of a table is using the
head/tail methods

```
titanic_sorted.head(3)
```

```
titanic_sorted.tail(3)
```

Note that nearly all methods in pandas return a new `Dataframe`, which means
that we can easily call another method on them

```
titanic_sorted.tail(10).head(5)  # select the first 5 of the last 10 passengers in the database
```

```
titanic_sorted.iloc[-10:-5]  # alternative way to get the same passengers
```

**Exercise**: use sorting and tail/head or indexing to find the 10 youngest
passengers on the titanic. Try to do this on a single line by chaining calls
to the titanic `DataFrame` object

```{.python .input}
titanic.sort_values...
```

### Indexing rows by value

One final way to select specific columns is by their value

```
titanic[titanic.sex == 'female']  # selects all females
```

```
# select all passengers older than 60 who departed from Southampton
titanic[(titanic.age > 60) & (titanic['embark_town'] == 'Southampton')]
```

Note that this required typing `titanic` quite often. A quicker way to get the
same result is using the `query` method, which is described in detail
[here](http://pandas.pydata.org/pandas-docs/stable/indexing.html#the-query-method)
(note that using the `query` method is also faster and uses a lot less
memory).

> You may have trouble using the `query` method with columns which have
a name that cannot be used as a Python identifier.

```
titanic.query('(age > 60) & (embark_town == "Southampton")')
```

When selecting a categorical multiple options from a categorical values you 
might want to use `isin`:
```
titanic[titanic['class'].isin(['First','Second'])]
```

Particularly useful when selecting data like this is the `isna` method which
finds all missing data

```
titanic[~titanic.age.isna()]  # select first few passengers whose age is not N/A
```

This removing of missing numbers is so common that it has is own method

```
titanic.dropna()  # drops all passengers that have some datapoint missing
```

```
titanic.dropna(subset=['age', 'fare'])  # Only drop passengers with missing ages or fares
```

**Exercise**: use sorting, indexing by value, `dropna` and `tail`/`head` or
indexing to find the 10 oldest female passengers on the titanic. Try to do
this on a single line by chaining calls to the titanic `DataFrame` object

```
titanic...
```

## Plotting the data

Before we start analyzing the data, let's play around with visualizing it.
Pandas does have some basic built-in plotting options:

```
titanic.fare.hist(bins=20, log=True)
```

```
titanic.age.plot()
```

To plot all variables simply call `plot` or `hist` on the full dataframe
rather than a single Series (i.e., column). You might want to set `subplots=True`
to plot each variable in a different subplot.

Individual Series are essentially 1D arrays, so we can use them as such in
`matplotlib`

```
plt.scatter(titanic.age, titanic.fare)
```

However, for most purposes much nicer plots can be obtained using
[Seaborn](https://seaborn.pydata.org). Seaborn has support to produce plots
showing the
[univariate](https://seaborn.pydata.org/tutorial/distributions.html#plotting-univariate-distributions)
or
[bivariate](https://seaborn.pydata.org/tutorial/distributions.html#plotting-bivariate-distributions)
distribution of data in a single or a grid of plots.  Most of the seaborn
plotting functions expect to get a pandas `DataFrame` (although they will work
with Numpy arrays as well). So we can plot age vs. fare like:

```
sns.jointplot('age', 'fare', data=titanic)
```

**Exercise**: check the documentation from `sns.jointplot` (hover the mouse
over the text `jointplot` and press shift-tab) to find out how to turn the
scatter plot into a density (kde) map

```
sns.jointplot('age', 'fare', data=titanic, ...)
```

Here is just a brief example of how we can use multiple columns to illustrate
the data in more detail

```
sns.relplot(x='age', y='fare', col='class', hue='sex', data=titanic,
           col_order=('First', 'Second', 'Third'))
```

**Exercise**: Split the plot above into two rows with the first row including
the passengers who survived and the second row those who did not (you might
have to check the documentation again by using shift-tab while overing the
mouse over `relplot`)

```
sns.relplot(x='age', y='fare', col='class', hue='sex', data=titanic,
           col_order=('First', 'Second', 'Third')...)
```

One of the nice thing of Seaborn is how easy it is to update how these plots
look. You can read more about that
[here](https://seaborn.pydata.org/tutorial/aesthetics.html). For example, to
increase the font size to get a plot more approriate for a talk, you can use:

```
sns.set_context('talk')
sns.violinplot(x='class', y='age', hue='sex', data=titanic, split=True,
               order=('First', 'Second', 'Third'))
```

## Summarizing the data (mean, std, etc.)

There are a large number of built-in methods to summarize the observations in
a Pandas `DataFrame`. Most of these will return a `Series` with the columns
names as index:

```
titanic.mean()
```

```
titanic.quantile(0.75)
```

One very useful one is `describe`, which gives an overview of many common
summary measures

```
titanic.describe()
```

For a more detailed exploration of the data, you might want to check 
[pandas_profiliing](https://pandas-profiling.github.io/pandas-profiling/docs/)
(not installed in fslpython, so the following will not run in fslpython):

```
from pandas_profiling import ProfileReport
profile = ProfileReport(titanic, title='Titanic Report', html={'style':{'full_width':True}})
profile.to_widgets()
```

Note that non-numeric columns are ignored when summarizing data in this way.

We can also define our own functions to apply to the columns (in this case we
have to explicitly set the data types).

```
def mad(series):
    """
    Computes the median absolute deviatation (MAD)

    This is a outlier-resistant measure of the standard deviation
    """
    no_nan = series.dropna()
    return np.median(abs(no_nan - np.nanmedian(no_nan)))

titanic.select_dtypes(np.number).apply(mad)
```

We can also provide multiple functions to the `apply` method (note that
functions can be provided as strings)

```
titanic.select_dtypes(np.number).apply(['mean', np.median, np.std, mad])
```

### Grouping by

One of the more powerful features of is `groupby`, which splits the dataset on
a categorical variable. The book contains a clear tutorial on that feature
[here](https://jakevdp.github.io/PythonDataScienceHandbook/03.08-aggregation-and-grouping.html). You
can check the pandas documentation
[here](http://pandas.pydata.org/pandas-docs/stable/groupby.html) for a more
formal introduction. One simple use is just to put it into a loop

```
for cls, part_table in titanic.groupby('class'):
    print(f'Mean fare in {cls.lower()} class: {part_table.fare.mean()}')
```

However, it is more often combined with one of the aggregation functions
discussed above as illustrated in this figure from the [Python data science
handbook](https://jakevdp.github.io/PythonDataScienceHandbook/06.00-figure-code.html#Split-Apply-Combine)

![group by image](group_by.png)

```
titanic.groupby('class').mean()
```

We can also group by multiple variables at once

```
titanic.groupby(['class', 'survived']).mean()  # as always in pandas supply multiple column names as lists, not tuples
```

When grouping it can help to use the `cut` method to split a continuous variable
into a categorical one

```
titanic.groupby(['class', pd.cut(titanic.age, bins=(0, 18, 50, np.inf))]).mean()
```

We can use the `aggregate` method to apply a different function to each series

```
titanic.groupby(['class', 'survived']).aggregate((np.median, mad))
```

Note that both the index (on the left) and the column names (on the top) now
have multiple levels. Such a multi-level index is referred to as `MultiIndex`.
This does complicate selecting specific columns/rows. You can read more of using
`MultiIndex` [here](http://pandas.pydata.org/pandas-docs/stable/advanced.html).
The short version is that columns can be selected using direct indexing (as
discussed above)

```
df_full = titanic.groupby(['class', 'survived']).aggregate((np.median, mad))
```

```
df_full[('age', 'median')]  # selects median age column; note that the round brackets are optional
```

```
df_full['age']  # selects both age columns
```

Remember that indexing based on the index was done through `loc`. The rest is
the same as for the columns above

```
df_full.loc[('First', 0)]
```

```
df_full.loc['First']

```

More advanced use of the `MultiIndex` is possible through `xs`:

```
df_full.xs(0, level='survived') # selects all the zero's from the survived index
```

```
df_full.xs('mad', axis=1, level=1) # selects mad from the second level in the columns (i.e., axis=1)
```

## Reshaping tables

If we were interested in how the survival rate depends on the class and sex of
the passengers we could simply use a groupby:

```
titanic.groupby(['class', 'sex']).survived.mean()
```

However, this single-column table is difficult to read. The reason for this is
that the indexing is multi-leveled (called `MultiIndex` in pandas), while there
is only a single column. We would like to move one of the levels in the index to
the columns. This can be done using `stack`/`unstack`:

- `unstack`: Moves one levels in the index to the columns
- `stack`: Moves one of levels in the columns to the index

```
titanic.groupby(['class', 'sex']).survived.mean().unstack('sex')
```

The former table, where the different groups are defined in different rows, is
often referred to as long-form. After unstacking the table is often referred to
as wide-form as the different group (sex in this case) is now represented as
different columns. In pandas some operations are easier on long-form tables
(e.g., `groupby`) while others require wide_form tables (e.g., making scatter
plots of two variables). You can go back and forth using `unstack` or `stack` as
illustrated above, but as this is a crucial part of pandas there are many
alternatives, such as `pivot_table`, `melt`, and `wide_to_long`, which we will
discuss below.

We can prettify the table further using seaborn

```
ax = sns.heatmap(titanic.groupby(['class', 'sex']).survived.mean().unstack('sex'),
                 annot=True)
ax.set_title('survival rate')
```

Note that there are also many ways to produce prettier tables in pandas (e.g.,
color all the negative values). This is documented
[here](http://pandas.pydata.org/pandas-docs/stable/style.html).

Because this stacking/unstacking is fairly common after a groupby operation,
there is a shortcut for it: `pivot_table`

```
titanic.pivot_table('survived', 'class', 'sex')
```

As usual in pandas, where we can also provide multiple column names

```
sns.heatmap(titanic.pivot_table('survived', ['class', 'embark_town'], ['sex', pd.cut(titanic.age, (0, 18, np.inf))]), annot=True)
```

We can also change the function to be used to aggregate the data

```
sns.heatmap(titanic.pivot_table('survived', ['class', 'embark_town'], ['sex', pd.cut(titanic.age, (0, 18, np.inf))],
                                aggfunc='count'), annot=True)
```

As in `groupby` the aggregation function can be a string of a common aggregation
function, or any function that should be applied.

We can even apply different aggregate functions to different columns

```
titanic.pivot_table(index='class', columns='sex',
                    aggfunc={'survived': 'count', 'fare': np.mean}) # compute number of survivors and mean fare

```

The opposite of `pivot_table` is `melt`. This can be used to change a wide-form
table into a long-form table. This is not particularly useful on the titanic
dataset, so let's create a new table where this might be useful. Let's say we
have a dataset listing the FA and MD values in various WM tracts:

```
tracts = ('Corpus callosum', 'Internal capsule', 'SLF', 'Arcuate fasciculus')
df_wide = pd.DataFrame.from_dict(dict({'subject': list('ABCDEFGHIJ')}, **{
    f'FA({tract})': np.random.rand(10) for tract in tracts }, **{
    f'MD({tract})': np.random.rand(10) * 1e-3 for tract in tracts
}))
df_wide
```

This wide-form table (i.e., all the information is in different columns) makes
it hard to select just all the FA values or only the values associated with the
SLF. For this it would be easier to list all the values in a single column.
Most of the tools discussed above (e.g., `group_by` or `seaborn` plotting) work
better with long-form data, which we can obtain from `melt`:

```
df_long = df_wide.melt('subject', var_name='measurement', value_name='dti_value')
df_long.head(12)
```

We can see that `melt` took all the columns (we could also have specified a
specific sub-set) and returned each measurement as a seperate row. We probably
want to seperate the measurement column into the measurement type (FA or MD) and
the tract name. Many string manipulation function are available in the
`DataFrame` object under `DataFrame.str`
([tutorial](http://pandas.pydata.org/pandas-docs/stable/text.html))

```
df_long['variable'] = df_long.measurement.str.slice(0, 2)  # first two letters correspond to FA or MD
df_long['tract'] = df_long.measurement.str.slice(3, -1)  # fourth till the second-to-last letter correspond to the tract
df_long.head(12)
```

Finally we probably do want the FA and MD variables as different columns.

**Exercise**: Use `pivot_table` or `stack`/`unstack` to create a column for MD
and FA.

```
df_unstacked = df_long.
```

We can now use the tools discussed above to visualize the table (`seaborn`) or
to group the table based on tract (`groupby` or `pivot_table`).

```
# feel free to analyze this random data in more detail
```

In general pandas is better at handling long-form than wide-form data, although
for better visualization of the data an intermediate format is often best. One
exception is calculating a covariance (`DataFrame.cov`) or correlation
(`DataFrame.corr`) matrices which computes the correlation between each column:

```
sns.heatmap(df_wide.corr(), cmap=sns.diverging_palette(240, 10, s=99, n=300), )
```

## Linear fitting (`statsmodels`)

Linear fitting between the different columns is available through the
[`statsmodels`](https://www.statsmodels.org/stable/index.html) library. A nice
way to play around with a wide variety of possible models is to use R-style
functions. The usage of the functions in `statsmodels` is described
[here](https://www.statsmodels.org/dev/example_formulas.html). You can find a
more detailed description of the R-style functions
[here](https://patsy.readthedocs.io/en/latest/formulas.html#the-formula-
language).

In short these functions describe the linear model as a string. For example,
`"y ~ x + a + x * a"` fits the variable `y` as a function of `x`, `a`, and the
interaction between `x` and `a`. The intercept is included by default (you can
add `"+ 0"` to remove it).

```
result = smf.logit('survived ~ age + sex + age * sex', data=titanic).fit()
print(result.summary())
```

Note that `statsmodels` understands categorical variables and automatically
replaces them with dummy variables.

Above we used logistic regression, which is appropriate for the binary
survival rate. A wide variety of linear models are available. Let's try a GLM,
but assume that the fare is drawn from a Gamma distribution:

```
age_dmean = titanic.age - titanic.age.mean()
result = smf.glm('fare ~ age_dmean + embark_town', data=titanic).fit()
print(result.summary())
```

Cherbourg passengers clearly paid a lot more...


Note that we did not actually add the `age_dmean` to the
`DataFrame`. `statsmodels` (or more precisely the underlying
[patsy](https://patsy.readthedocs.io/en/latest/) library) automatically
extracted this from our environment. This can lead to confusing behaviour...

# More reading

Other useful features

- [Concatenating and merging tables](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/08_combine_dataframes.html)
- [Lots of time series support](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/09_timeseries.html)
- [Rolling Window
  functions](http://pandas.pydata.org/pandas-docs/stable/computation.html#window-
  functions) for after you have meaningfully sorted your data
- and much, much more
