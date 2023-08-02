import random

def probability_at_least_3_red_balls_no_green(green_balls, red_balls, blue_balls, num_balls):
  """
  Calculates the probability that at least 3 of 15 balls drawn from a jar with
  green, red, and blue balls are red and none are green.

  Args:
    green_balls: The number of green balls in the jar.
    red_balls: The number of red balls in the jar.
    blue_balls: The number of blue balls in the jar.
    num_balls: The number of balls drawn.

  Returns:
    The probability that at least 3 of the balls drawn are red and none are green.
  """

  probability_of_3_red_balls = (
      (red_balls ** 3) * (green_balls ** 12) * (blue_balls ** 0)) / (
          (red_balls + green_balls + blue_balls) ** 15)
  probability_of_4_red_balls = (
      (red_balls ** 4) * (green_balls ** 11) * (blue_balls ** 0)) / (
          (red_balls + green_balls + blue_balls) ** 15)
  probability_of_5_red_balls_or_more = 1 - (
      probability_of_3_red_balls + probability_of_4_red_balls)

  return probability_of_5_red_balls_or_more

if __name__ == "__main__":
  probability = probability_at_least_3_red_balls_no_green(
      green_balls=1875, red_balls=31, blue_balls=5595, num_balls=15)
  print(probability)
