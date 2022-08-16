# Objetive

To get cryptocurrencies' data daily and forecasting over them was decided to create this project who seeks to do these two thing and provide a API who can call and give back these data for others projects.

# Architecture

This project's architecture is a union of the architecture from the "Cookiecutter" and the "Clean Architecture", creating, then, a perfect architecture for model development and deployment together, below is possible to see the locations of every thing:

- **data**: all data for modeling (isn't in github). 
- **docs**: documentations explaining about this software's creation and commits.
- **domain**: all code of the API.
- **logs**: all logs of the modeling process.
- **cloudbuild.yaml**: auxiliary file for the CI / CD process.
- **Dockerfile**: contais all instrunctions to build the docker image.
- **requirements.txt**: contains all libs necessary for the API's development.
- **.github**: contains all instrunctions to CI / CD process with Github Actions.