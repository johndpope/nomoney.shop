# nomoney.shop
[![Django CI](https://github.com/snake-soft/nomoney.shop/workflows/Django%20CI/badge.svg)](https://github.com/snake-soft/nomoney.shop/actions)
[![Build Status](https://travis-ci.org/snake-soft/nomoney.shop.svg?branch=master)](https://travis-ci.org/snake-soft/nomoney.shop)
[![Documentation Status](https://readthedocs.org/projects/nomoneyshop/badge/?version=latest)](https://nomoneyshop.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/snake-soft/nomoney.shop/badge.svg?branch=master)](https://coveralls.io/github/snake-soft/nomoney.shop?branch=master)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
---
:us: This year, 2020, the world economy as a guarant of wealth is going to get damaged.
Currently the 'experts' have a huge spread of future predictions.

That is why I created this project.

It's purpose is to deliver people with the needed goods and services without the need to buy with money.

Easyly list down the things you are searching for and do the same with things you can offer therefore.
If there is another user, offering the things you search and searching what your offer, you guessed it, it will show you the possible deal.

Often these kind of deals aren't possible.
The following constellation is more common:
- A has what B needs and needs what C has
- B  has what C needs and needs what A has
- C  has what A needs and needs what B has

Being not easy to be calculated this kind of deal is easy to calculate for a computer.

---
:de: In diesem Jahr, 2020, steht die Weltwirtschaft als Garant für unseren Wohlstand auf einer harten Probe. Derzeit haben die "Experten" eine große Bandbreite an Zukunftsprognosen.

Deshalb habe ich dieses Projekt erstellt.

Ziel ist es, dass die Menschen sich mit den benötigten Waren und Dienstleistungen versorgen können, auch wenn kein Geld als Zahlungsmittel mehr vorhanden ist. 

Liste einfach die Dinge auf, nach denen du suchst, und mache dasselbe mit den Dingen, die du dafür anbieten können.
Wenn es einen anderen Benutzer gibt, der die von Ihnen gesuchten Dinge anbietet und nach Ihrem Angebot sucht, haben Sie es erraten. Dies zeigt Ihnen das mögliche Geschäft.

Oft sind solche Geschäfte nicht möglich. Die folgende Konstellation ist häufiger:
- A hat was B braucht und braucht was C hat
- B hat was C braucht und braucht was A hat
- C hat was A braucht und braucht was B hat

Da es nicht einfach ist, diese Art von Geschäft zu berechnen, überlassen wir das der Rechenmaschine.


---
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
Have a look at the [documentation](https://nomoneyshop.readthedocs.io/en/latest/).

### Introducing notes
- Clone it, use it, extend it


### Prerequisites
It should work with lower Python versions but tests are running on 3.5 and 3.8.

This project makes use of the following libraries:
* [Django](https://docs.djangoproject.com/en/) - The web framework for perfectionists with deadlines.


### Installing
Local install running the development server:
```
git clone git@github.com:snake-soft/nomoney.shop.git
cd nomoney.shop

virtualenv -p python3 venv
source venv/bin/activate

pip install -r requirements.txt

python3 manage.py createsuperuser
python3 manage.py migrate
python3 manage.py runserver
```

After that go into config/settings directory. 
Copy data_sample.py to data.py, open and modify the data inside.


You can install the latest release from pip:
```
pip install nomoney.shop
```


### Short example
```python
...
```


## Running the tests
Rename 'secrets.sample.py' in tests directory to 'secrets.py' and include your e-mail account for testing.
Then run this inside root directory:
```
...
```
or run it with coverage:
```
...
```


### And coding style tests
Code style is not finished, mostly because of missing docstrings.
```
...
```


## Deployment
This project is not ready to be deployed productive


## Contributing
Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Versioning
We use [SemVer](http://semver.org/) for versioning.


## Authors
* **Me** - *Initial work* - [Snake-Soft](https://github.com/snake-soft)

See also the list of [contributors](https://github.com/snake-soft/nomoney.shop/graphs/contributors) who participated in this project.


## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
