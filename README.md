# Technical Track of Computer Tools for Linguistic Research (2022/2023)

As a part of a compulsory course
[Computer Tools for Linguistic Research](https://www.hse.ru/edu/courses/749661034)
in [National Research University Higher School of Economics](https://www.hse.ru/).

This technical track is aimed at building basic skills for retrieving data from external
WWW resources and processing it for future linguistic research. The idea is to automatically
obtain a dataset that has a certain structure and appropriate content,
perform morphological analysis using various natural language processing (NLP)
libraries. [Dataset requirements](./docs/public/dataset.md).

Instructors:

* [Khomenko Anna Yurievna](https://www.hse.ru/org/persons/65858472) - linguistic track lecturer
* [Lyashevskaya Olga Nikolaevna](https://www.hse.ru/staff/olesar) - linguistic track lecturer
* [Demidovskij Alexander Vladimirovich](https://www.hse.ru/staff/demidovs#sci) - technical track lecturer
* [Uraev Dmitry Yurievich](https://www.hse.ru/org/persons/208529395) - technical track practice lecturer
* [Kashchikhin Andrei Nikolaevich](https://t.me/WhiteJaeger) - technical track expert
* [Kazyulina Marina Sergeevna](https://t.me/poemgranate) - technical track assistant
* [Zharikov Egor Igorevich](https://t.me/godb0i) - technical track assistant
* [Novikova Irina Alekseevna](https://t.me/iriinnnaaaaa) - technical track assistant
* [Blyudova Vasilisa Mikhailovna](https://t.me/Vasilisa282) - technical track assistant
* [Zaytseva Vita Vyacheslavovna](https://t.me/v_ttec) - technical track assistant

## Project Timeline

1. **Scrapper**:
   1. Short summary: Your code can automatically parse a media website you are going to choose,
      save texts and its metadata in a proper format.
   2. Deadline: **April, 14**
   3. Format: each student works in their own PR.
   4. Dataset volume: 5-7 articles.
   5. Design document: [`./lab_5_scrapper/README.md`](./lab_5_scrapper/README.md).
   6. List of media websites to select from: at the `Resources` section on this page.
2. **Pipeline**:
   1. Short summary: Your code can automatically process raw texts from previous step,
      make point-of-speech tagging and basic morphological analysis.
   2. Deadline: **May, 12**
   3. Format: each student works in their own PR.
   4. Dataset volume: 5-7 articles.
   5. Design document: [`./lab_6_pipeline/README.md`](./lab_6_pipeline/README.md)

## Lectures history

|    Date    | Lecture topic                                       | Important links              |
|:----------:|:----------------------------------------------------|:-----------------------------|
| 13.03.2023 | **Lecture:** Introduction to technical track.       | [Lab no. 5 description][7]   |
| 17.03.2023 | **Seminar:** 3rd party libraries.                   | N/A                          |
| 20.03.2023 | **Lecture:** Requests and `HTML`.                   | [Listing][8]                 |
| 24.03.2023 | **Seminar:** Headers and introduction to `bs4`.     | [Listing][12]                |
| 27.03.2023 | **EXAM WEEK:** skipping lecture and seminars.       | N/A                          |
| 03.04.2023 | **Lecture:** Access file system via `pathlib`.      | [Listing][13], [Listing][14] |
| 07.04.2023 | **Seminar:** Early version of `HTMLParser`.         | [Listing][15]                |
| 10.04.2023 | **Lecture:** Working with dates via `datetime`.     | [Listing][16]                |
| 14.04.2023 | **First deadline:** crawler assignment.             | N/A                          |
| 17.04.2023 | **Lecture:** Assignment no. 6: concept and details. | N/A                          |
| 21.04.2023 | **Seminar:** `CorpusManager` implementation.        | N/A                          |
| 24.04.2023 | **Lecture:** Automated morphological analysis.      | [Listing][17], [Listing][18] |
| 28.04.2023 | **Seminar:** `pymystem3`API.                        | [Listing][17], [Listing][18] |
| 01.05.2023 | **HOLIDAYS:** skipping lecture and seminars.        | N/A                          |
| 05.05.2023 | **HOLIDAYS:** skipping lecture and seminars.        | N/A                          |
| 08.05.2023 | **HOLIDAYS:** skipping lecture and seminars.        | N/A                          |
| 12.05.2023 | **Second deadline:** pipeline assignment.           | N/A                          |

You can find a more complete summary from lectures as a
[list of topics](./docs/public/lectures_content.md).

## Technical solution

| Module                | Description                        | Component          | Need to get |
|:----------------------|:-----------------------------------|:-------------------|:------------|
| [`pathlib`][1]        | working with file paths            | scrapper           | 4           |
| [`requests`][2]       | downloading web pages              | scrapper           | 4           |
| [`BeautifulSoup4`][3] | finding information on web pages   | scrapper           | 4           |
| [`lxml`][4]           | **Optional** parsing HTML          | scrapper           | 6           |
| `datetime`            | working with dates                 | scrapper           | 6           |
| `json`                | working with json text format      | scrapper, pipeline | 4           |
| [`pymystem3`][5]      | module for morphological analysis  | pipeline           | 6           |
| [`pymorphy2`][6]      | module for morphological analysis  | pipeline           | 10          |

Software solution is built on top of three components:
1. [`scrapper.py`](./lab_5_scrapper/scrapper.py) - a module for finding articles
   from the given media, extracting text and
   dumping it to the file system. Students need to implement it.
2. `pipeline.py` - a module for processing text: point-of-speech tagging and
   basic morphological analysis. Students need to implement it.
3. [`article.py`](core_utils/article/article.py) - a module for article abstraction
   to encapsulate low-level manipulations with the article.

## Handing over your work

Order of handing over:

1. Lab work is accepted for oral presentation.
2. A student has explained the work of the program and showed it in action.
3. A student has completed the min-task from a mentor that requires some slight code modifications.
4. A student receives a mark:
   1. That corresponds to the expected one, if all the steps above are completed and mentor is
      satisfied with the answer.
   2. One point bigger than the expected one, if all the steps above are completed and
      mentor is very satisfied with the answer.
   3. One point smaller than the expected one, if a lab is handed over one week later than the
      deadline and criteria from 4.1 are satisfied.
   4. Two points smaller than the expected one, if a lab is handed over more than one week later
      than the deadline and criteria from 4.1 are satisfied.

> NOTE: A student might improve their mark for the lab, if they complete
> tasks of the next level after handing over the lab.

A lab work is accepted for oral presentation if all the criteria below are satisfied:

1. There is a Pull Request (PR) with a correctly formatted name:
   `Scrapper, <NAME> <SURNAME> - <UNIVERSITY GROUP NAME>`.
   Example: `Scrapper, Valeriya Kuznetsova - 19FPL1`.
2. Has a filled file `target_score.txt` with an expected mark.
   Acceptable values: 4, 6, 8, 10.
3. Has green status.
4. Has a label `done`, set by mentor.

## Resources

1. Academic performance: [link][9]
2. Media websites list: [link][10]
3. Python programming course from previous semester: [link][11]
4. Scrapping tutorials: [YouTube series (russian)](https://youtu.be/7hn1_t2ZtJQ)
5. [HOWTO: Set up your fork](./docs/public/starting_guide.md)
6. [HOWTO: Running tests](./docs/public/tests.md)
7. [HOWTO: Running assignments in terminal](./docs/public/run_in_terminal.md)

[1]: https://pypi.org/project/pathlib/
[2]: https://pypi.org/project/requests/2.25.1/
[3]: https://pypi.org/project/beautifulsoup4/4.11.1/
[4]: https://pypi.org/project/lxml/
[5]: https://pypi.org/project/pymystem3/
[6]: https://pypi.org/project/pymorphy2/
[7]: ./lab_5_scrapper/README.md
[8]: ./seminars/seminar_03_20_2023/try_requests.py
[9]: https://docs.google.com/spreadsheets/d/19DS6F6_NrgjGbLUjFm9-REuuaECvApEW_o4pHvaXyLQ
[10]: https://docs.google.com/spreadsheets/d/11mmZCKW0WK7rZlpg3eOBA074zwWiXgJjivVUIdDe6-E
[11]: https://github.com/fipl-hse/2022-2-level-labs
[12]: ./seminars/seminar_03_24_2023/try_beautiful_soup.py
[13]: ./seminars/seminar_04_03_2023/try_json.py
[14]: ./seminars/seminar_04_03_2023/try_fs.py
[15]: ./seminars/seminar_04_07_2023/try_html_parser.py
[16]: ./seminars/seminar_04_10_2023/try_dates.py
[17]: ./seminars/seminar_04_24_2023/try_pymystem.py
[18]: ./seminars/seminar_04_24_2023/try_pymorphy.py
