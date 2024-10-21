# Análisis Exploratorio de Datos (EDA) del Dataset de Jugadores de FIFA y estadísticas reales

_[FifaStats-RealGoals]_

## Descripción del Proyecto

Este proyecto se centra en la realización de un Análisis Exploratorio de Datos (EDA) utilizando un dataset que contiene información sobre jugadores de FIFA y sus estadísticas reales. El objetivo es explorar, visualizar y analizar los datos para identificar patrones, tendencias y correlaciones entre las características de los jugadores y sus actuaciones en el mundo real.
Hay un objetivo ulterior que se trata de obtener patrones que permitan no solo un analisis descriptivo como el que se pretende en el presente trabajo sino poder utilizar modelos de Machine Learning para poder hacer pode hacer análisis predictivos de comportamientos en base a los patrones obtenidos.

## Presentación

<[URL para ver la presentación del trabajo](https://gamma.app/docs/ssgpco10m2u6cs5?following_id=fary9hjdj3f1jyn&follow_on_start=true)>

## 🔧 Herramientas y librerías utilizadas
Python, Numpy, Pandas, Matplotlib y Seaborn entre otras. Con especial mención a Selenium para poder llevar a cabo toda la parte de Web Scrapping 🔍 y construcción de la base de datos final para el trabajo realizado.


## Contenido del Dataset

El dataset está compuesto por dos datasets, uno obtenido por kaggel con los datos del fifa 2022, el cual incluye las siguientes columnas:

sofifa_id player_url short_name long_name player_positions overall potential value_eur wage_eur age dob height_cm weight_kg club_team_id club_name league_name league_level club_position club_jersey_number club_loaned_from club_joined club_contract_valid_until nationality_id nationality_name nation_team_id nation_position nation_jersey_number preferred_foot weak_foot skill_moves international_reputation work_rate body_type real_face release_clause_eur player_tags player_traits pace shooting passing dribbling defending physic attacking_crossing attacking_finishing attacking_heading_accuracy attacking_short_passing attacking_volleys skill_dribbling skill_curve skill_fk_accuracy skill_long_passing skill_ball_control movement_acceleration movement_sprint_speed movement_agility movement_reactions movement_balance power_shot_power power_jumping power_stamina power_strength power_long_shots mentality_aggression mentality_interceptions mentality_positioning mentality_vision mentality_penalties mentality_composure defending_marking_awareness defending_standing_tackle defending_sliding_tackle goalkeeping_diving goalkeeping_handling goalkeeping_kicking goalkeeping_positioning goalkeeping_reflexes goalkeeping_speed ls st rs lw lf cf rf rw lam cam ram lm lcm cm rcm rm lwb ldm cdm rdm rwb lb lcb cb rcb rb gk player_face_url club_logo_url club_flag_url nation_logo_url nation_flag_url

Mientras que el otro es un dataset creado por mi a través de un web scrapping, el cual contiene las siguientes columnas:
nombre match_id posicion pj pt goles asistencias tarjetas equipo porteria

## Objetivos del Análisis

1. Exploración de Datos: Comprender la estructura del dataset, la distribución de las variables y la calidad de los datos.
2. Visualización: Crear gráficos y visualizaciones que ayuden a ilustrar las relaciones y tendencias en los datos.
3. Identificación de Patrones: Detectar patrones en el rendimiento de los jugadores en función de diferentes características (edad, posición, valor de mercado, etc.).
4. Correlación: Analizar las correlaciones entre diferentes variables y cómo afectan el rendimiento general de los jugadores.

## Herramientas Utilizadas

-   _Python_: Lenguaje de programación utilizado para el análisis.
-   _Pandas_: Biblioteca para la manipulación y análisis de datos.
-   _Matplotlib y Seaborn_: Bibliotecas para la visualización de datos.
-   _Jupyter Notebook_: Entorno de desarrollo interactivo para ejecutar y documentar el análisis.

## Cómo Ejecutar el Proyecto

1. Clona este repositorio en tu máquina local:
   git clone <[URL del repositorio](https://github.com/2012FranMartinez/FifaStats-RealGoals.git)>
2. Navega al directorio del proyecto:
   cd <nombre del directorio>
3. Abre el notebook Jupyter:
   jupyter notebook
4. ¡¡¡AVISO CHROMEDRIVER!!!
   Si quieres utilizar la parte del scraping, _tienes que descargar el chromedriver_ según la versión del google chrome que tengas de <[ChromeDriver Downlads](https://developer.chrome.com/docs/chromedriver/downloads?hl=es-419)>

Ejecuta las celdas para realizar el análisis.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea tu rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz un commit (git commit -m 'Añadir nueva funcionalidad').
4. Haz un push a tu rama (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request.

## Futuras lineas del proyecto

-   Hacer lo mismo con los años del 15-21 y 23-25 Goles
-   Hacer lo mismo con los años del 15-21 y 23-25 Asistencia
-   Hacer lo mismo con los años del 15-21 y 23-25 Tarjetas
-   Hacer lo mismo con los años del 15-21 y 23-25 Faltas
-   Mejorar scraping
-   Mejorar obtención Id fifa (fusión datasets)
-   Llevarlo a un proyecto de ML

## Contacto

Para más información, por favor contacta a 2012franmartinez@gmail.com
