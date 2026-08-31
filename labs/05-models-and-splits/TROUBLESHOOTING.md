# Troubleshooting

The split experiment requires a saved prediction. In a script, use:

~~~bash
uv run tinyml-maintenance lab predict split --choice A --reason "Rows from one machine may cross the boundary."
~~~

Do not treat a random row as independent. Sensor readings from one machine share type, site, age, history, and operating conditions.

Random forest was selected by validation average precision. Gradient boosting's slightly higher test AP is visible only after selection and cannot be used to change the winner.
