# Working with UD format and `CONLL-U`

During the implementation of Lab 6, you need to convert Mystem and PyMorphy tags to the UD format
and save in a `.conllu` file. Here you will learn what Mystem and PyMorphy tags look like,
how to convert them to the UD format and what should `.conllu` file structure look like.

> **NOTE**: UD (Universal Dependencies) is a framework for consistent annotation of grammar
> (parts of speech, morphological features, and syntactic dependencies) across different
> human languages.
> All this annotation is usually stored in a format called `CONLL-U`, that is a vertical,
> table-like format.

* [Mystem and PyMorphy to UD](#mystem-pymorphy-to-ud)
  * [UD](#ud)
  * [Mystem](#mystem)
  * [PyMorphy](#pymorphy)
* [`CONLL-U` structure](#conllu-structure)

## <a name="mystem-pymorphy-to-ud"></a>Mystem and PyMorphy to UD

The number of available morphological features in PyMorphy, Mystem and UD is big. It would require
a lot of work to make a perfect mapping of the features from one system to another.
This section describes how to parse the output from PyMorphy and Mystem and convert a **part of
the available morphological features** to the UD format.

You need to convert the following features:

* POS (Part of speech)
* Case
* Number
* Gender
* Animacy
* Tense

As different parts of speech have different tags (for example: **verbs** have **tense** while
**nouns** do not), it is important to make the parsing per part of speech.

To convert them from one system to another,
it is necessary to understand how each system is structured.

### <a name="ud"></a>UD

The UD format for storing morphological information is structured as follows:
`FeatureName=Value|FeatureName=Value|FeatureName=Value...`
where `FeatureName` is a name of the morphological feature of the token (for example, `Number`)
and `Value` is the actual value of the feature (for example, `Sing` - short for singular).

For example:

* `Animacy=Inan|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing`
  * `Animacy=Inan` - inanimate
  * `Case=Acc` - accusative case
  * `Degree=Pos` - degree of comparison: positive/first degree
  * `Gender=Masc` - masculine gender
  * `Number=Sing` - singular number

> **NOTE**: The list of all tags used in the UD system is available on
> the [dedicated page](https://universaldependencies.org/u/feat/index.html).

### <a name="mystem"></a>Mystem

The `pymystem3` library is a wrapper around Mystem for Python.
It provides the morphological analysis for the language tokens.

> **NOTE**: The list of all tags used in Mystem is available on
> the [dedicated page](https://yandex.ru/dev/mystem/doc/grammemes-values.html).

It is structured as follows:
`POS,FeatureValue?,FeatureValue?...=(FeatureValue?,FeatureValue?...|FeatureValue?,FeatureValue?...|)`
where:

* `POS` is a part of speech
* `FeatureValue` is the value of a morphological feature
* `?` means that the value might not be present
* `|` means that there are several possible sets of morphological features for the token

The specific structure varies based on the part of speech, see examples below:

* Noun: `S,муж,од=(вин,ед|род,ед)` OR `S,жен,од=им,ед` OR `S,сокр=(пр,мн|пр,ед|вин,мн|вин,ед|дат,мн|дат,ед)`
* Adjective: `A=(вин,ед,полн,муж,од|род,ед,полн,муж|род,ед,полн,сред)` OR `A=(вин,мн,полн,неод|им,мн,полн)`
* Verb: `V,нп=прош,мн,изъяв,сов` OR `V,пе=(прош,ед,прич,кр,муж,сов,страд|непрош,мн,изъяв,3-л,сов)`
* Numeral-Adjective: `ANUM=(пр,ед,жен|дат,ед,жен|род,ед,жен|твор,ед,жен|)`
* Pronoun-Adjective: `APRO=(пр,мн|дат,мн|род,мн|твор,мн|им,мн|им,ед,жен|вин,ед,муж,од|род,ед,муж|род)`
* Numeral: `NUM=(им|вин,неод)`
* Pronoun: `SPRO,ед,3-л,жен=им` OR `SPRO,ед,3-л,жен=(дат|твор)`
* Particle, preposition, interjection, conjunction, part of a compound word, adverb, pronominal
  adverb: `PART=`, `PR=`, `INTJ=`, `CONJ=`, `COM=`, `ADV=`, `ADVPRO=` respectively

>**HINT**: For the mark 8 (when you have to fill the FEATS field information in the resulting
> `.conllu` file) there is no need to process `PART`, `PR`, `INTJ`, `CONJ`,
> `COM`, `ADVPRO`, `ADV` as they only have POS.

As it is seen from the examples above, the number of features can be different even for the
same part of speech:
compare `S,жен,од=им,ед` and `S,сокр=(пр,мн|пр,ед|вин,мн|вин,ед|дат,мн|дат,ед)`.
This fact should be kept in mind while parsing the morphological features.

> **NB**: For the sake of simplicity, only the first possible set of features is considered.
> For example, in this set of features`(вин,ед|род,ед)` you should consider this one `вин,ед`.

> **HINT**: As the `pymystem3` returns these morphological features as a string, there is nothing
> left but to parse it by delimiters (`,=|()`) or find more elegant way.

Let's parse `S,муж,од=(вин,ед|род,ед)` to the UD format.
As the morphological features in the UD format are structured as following:

* `FeatureName=Value|FeatureName=Value|FeatureName=Value...`

the resulting string for our example would be:

* `Animacy=Anim|Case=Acc|Gender=Masc|Number=Sing`

> **NB**: The complete mapping of features from Mystem to the UD format can be found in
> the [`ud_mapping.md`](ud_mapping.md).

> **HINT**: It's mandatory to use `Loc` mapping for pymystem3 `пр` case because
> in Slavic languages this is the only case that is used exclusively in combination with prepositions.
> A more detailed information you san see [here](https://universaldependencies.org/ru/feat/Case.html).

### <a name="pymorphy"></a>PyMorphy

PyMorphy uses the tags from OpenCorpora. The list of all tags is available on
the [OpenCorpora Website](http://opencorpora.org/dict.php?act=gram&order=priority).

As the `pymorphy2` returns these morphological features as an instance of the `OpencorporaTag`
class, it is possible to access its attributes to extract the information.

Available attributes for `OpencorporaTag` are:

* `POS`
* `animacy`
* `aspect`
* `case`
* `gender`
* `involvement`
* `mood`
* `number`
* `person`
* `tense`
* `transitivity`
* `voice`

They can be accessed as, for example, `tags.animacy` where `tags` is an instance of the
`OpencorporaTag` class.

Let's parse `OpencorporaTag('NOUN,anim,masc sing,nomn')` to the UD format.
As the morphological features in the UD format are structured as following:

* `FeatureName=Value|FeatureName=Value|FeatureName=Value...`

the resulting string for our example would be:

* `Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing`

> **NB**: The complete mapping of features from PyMorphy to the UD format can be found in
> the [`ud_mapping.md`](ud_mapping.md).

## <a name="conllu-structure"></a>`CONLL-U` structure

After processing your articles and converting Mystem and PyMorphy tags to the UD format,
you should save your annotated data in a `.conllu` file.

Let's look at an example of a `.conllu` file that should work for you.
It is a subset of a file from
[this repository](https://github.com/UniversalDependencies/UD_Russian-SynTagRus).
File with example text can be found [here](ud_test.conllu).

It has the following structure, where each "column" is responsible for:

* **ID**: Word index, integer starting at 1 for each new word in the sentence.
* **FORM**: Word form or punctuation symbol.
* **LEMMA**: Lemma or stem of word form.
* **UPOS**: Universal POS tag, mark as `X` if it is unspecified.
* **XPOS**: Language-specific POS tag.
  * **NB**: mark as `_` as we do not use it.
* **FEATS**: List of morphological features structured as
   `FeatureName=Value|FeatureName=Value|FeatureName=Value...` as per UD format;
   mark as `_` if not available.
* **HEAD**: Head of the current word.
  * **NB**: mark as `0` as we do not use it.
* **DEPREL**: Universal dependency relation to the HEAD.
  * **NB**: mark as `root` as we do not use it.
* **DEPS**: Enhanced dependency graph in the form of a list of head-deprel pairs.
  * **NB**: mark as `_` as we do not use it.
* **MISC**: Any other annotation.
  * **NB**: mark as `_` as we do not use it.

Thus, during the implementation of the Lab 6, you will work with the following "columns":
**ID**, **FORM**, **LEMMA**, **UPOS**, **FEATS**.
Fill in the rest of the "columns" as indicated in the structure above.

In addition, you must take into account that:

* New sentences start with the token ID being `1`;
* Fields cannot be empty. If no value for a field, the `_` is used;
* Comments usually consist of the sentences and are denoted using `#`.

Let's explain the second line
`2 советский советский ADJ _ Animacy=Inan|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing 3 amod 3:amod _`:

* `2` - ID
* `советский` - text of the token
* `советский` - lemma of the token
* `ADJ` - POS
* `_` - language specific POS; none in this case
* `Animacy=Inan|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing` - morphological features of the token
as per [tags](https://universaldependencies.org/u/feat/index.html):
  * `Animacy=Inan` - inanimate
  * `Case=Acc` - accusative case
  * `Degree=Pos` - degree of comparison: positive/first degree
  * `Gender=Masc` - masculine gender
  * `Number=Sing` - singular number
* `3` - the ID of the HEAD for the current token. HEAD is `период` in this case
* `amod` - relation to the HEAD token. `amod` - adjectival modifier
as per [tags](https://universaldependencies.org/u/dep/amod.html)
* `3:amod` - pair of HEAD:RELATION for the current token
* `_` - any other annotation; none in this case

> **NOTE**: More information about the structure of the `CONLL-U` format is available on
> the [dedicated page](https://universaldependencies.org/format.html).
