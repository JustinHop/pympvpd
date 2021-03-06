"""pympvpd.sample."""


def hello(name):
    """Respond hello.

    :rtype: str
    :return: "Hello `name`."

    :param str name: user name.

    >>> hello('Alice')
    'Hello, Alice.'
    """
    return 'Hello, {0}.'.format(name)


def bmi(height, weight):
    """Respond BMI.

    :rtype: float
    :return: Body mass index.

    :param float height: height (meters).
    :param float weight: weight (kilo grams).

    >>> bmi(1.68, 67.0)
    23.738662131519277
    """
    return weight / height ** 2
