# Testing methods
The testing for this project consists mainly of testing the different functions within 
the game both manually and automatically. For example, some functions that are tested are the function to move the player
given an input, the function to move the logs and turtles, and the function to remove the cars
once they travel off-screen, among others. In most cases, the automatic testing is done by creating a
mock object within the test function and manipulating that object for the purposes of the test.
The general way we go about testing with these mock objects is to call the function in question
on the mock object and then assert whether the actual new state of the object is equal to the
expected new state of the object. 

The manual testing consists of playing the game and making sure it responds to inputs as
expected. Mostly this involves making sure the game opens and runs properly,  moving the
player around and making sure the player dies and restarts at the beginning upon hitting an
obstacle, and assuring that the graphics appear like they should.