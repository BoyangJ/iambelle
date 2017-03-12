/*
  Hello World.ino
  2013 Copyright (c) Seeed Technology Inc.  All right reserved.
  Author:Loovee
  2013-9-18
  Grove - Serial LCD RGB Backlight demo.
  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.
  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.
  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <Wire.h>
#include "rgb_lcd.h"
#include <rgb_lcd.h>

rgb_lcd lcd;

//GLOBAL VARIABLES
int colourR;
int colourG;
int colourB;
int randnumber = 7; //seven is the most random number
int num_chars; //variable for number of characters in string
int ledPin3 = 3;
int ledPin2 = 2;
int ledPin4 = 4;
int ledPin7 = 7;

int colourflash_time = 440; //length of time in ms that colours will flash

//****************************************************************************************************************

void setup() 
{
    /* This arduino code is called when a nice tweet has been sent by Belle Bot, the nice twitter bot*/
    //INITIALIZATION
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);

    //seed random number for RNG
    randomSeed(analogRead(0)); 

    //set LED pins to light heart
    pinMode(ledPin2, OUTPUT);
    pinMode(ledPin4, OUTPUT);
    pinMode(ledPin3, OUTPUT);
    pinMode(ledPin7, OUTPUT);

    
    digitalWrite(ledPin2, HIGH); //set leds on. Light up da heart!
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin7, HIGH);
    //Set LCD colour
    colourR = 150;
    colourG = 150;
    colourB = 150;
    lcd.setRGB(colourR, colourG, colourB);
    lcd.setCursor(0, 0);
    lcd.print(":o "); //omg message coming!
    delay(3500);    

    digitalWrite(ledPin2, HIGH); //set leds on. Light up da heart!
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin7, HIGH);
    delay(1000);
    
    //set LCD display colour red
    colourR = 255;
    colourG = 0;
    colourB = 0;
    lcd.setRGB(colourR, colourG, colourB);    
    lcd.setCursor(0, 0); //first line
    lcd.print("Love has been");
    lcd.setCursor(0, 1); //second line
    lcd.print("dispensed!");
    delay(colourflash_time);
    //set LCD display colour
    colourR = 255;
    colourG = 0;
    colourB = 255;
    lcd.setRGB(colourR, colourG, colourB); //purple
        //turn heart lights off
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin4, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin7, LOW);
    delay(colourflash_time);
    colourR = 0;
    colourG = 0;
    colourB = 255;
    lcd.setRGB(colourR, colourG, colourB);  //blue
    digitalWrite(ledPin2, HIGH); //set leds on. Light up da heart!
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin7, HIGH);
    delay(colourflash_time);
    colourR = 0;
    colourG = 255;
    colourB = 255;
    lcd.setRGB(colourR, colourG, colourB); //cyan
        //turn heart lights off
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin4, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin7, LOW);
    delay(colourflash_time);
    colourR = 0;
    colourG = 255;
    colourB = 0;
    lcd.setRGB(colourR, colourG, colourB); //green
    digitalWrite(ledPin2, HIGH); //set leds on. Light up da heart!
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin7, HIGH);
    delay(colourflash_time);
    colourR = 255;
    colourG = 255;
    colourB = 0;
    lcd.setRGB(colourR, colourG, colourB); //yellow
    //turn heart lights off
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin4, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin7, LOW);
    delay(colourflash_time);
    digitalWrite(ledPin2, HIGH); //set leds on. Light up da heart!
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin7, HIGH);

    //screen backlight to white to display subsequent messages
    int whiteval = 100;
    colourR = whiteval;
    colourG = whiteval;
    colourB = whiteval;
    lcd.setRGB(colourR, colourG, colourB); //white
    lcd.clear();
    delay(3000); 
    //turn heart lights off
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin4, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin7, LOW);

    //ready cursor
    lcd.setCursor(0, 0);
    //set LED pins to input to save power
    pinMode(ledPin2, INPUT);
    pinMode(ledPin4, INPUT);
    pinMode(ledPin3, INPUT);
    pinMode(ledPin7, INPUT);
}

void loop() 
{
    //clear screen
    lcd.clear();
    
    /*INTERIM TEXT DISPLAY
    Making more friends...
    Thinking nice thoughts...
    Checking you out...
    You're the real belle!
    Hmmm...
     */ 
    randnumber = random(13);
    if(randnumber == 0){
      lcd.setCursor(15, 0); // set the cursor to column 15, line 0 (to start on right side of screen)
      lcd.print("Let's be friends :)");
      num_chars = strlen("Let's be friends :)");
    }else if(randnumber == 1){
      lcd.setCursor(15, 0);
      lcd.print("Thinking nice thoughts...");
      num_chars = strlen("Thinking nice thoughts...");
    }else if(randnumber == 2){
      lcd.setCursor(15, 0);
      lcd.print("I'm checking you out...");
      num_chars = strlen("I'm Checking you out...");
    }else if(randnumber == 3){
      lcd.setCursor(15, 0);
      lcd.print("You're the real belle!");
      num_chars = strlen("You're the real belle!");
    }else if(randnumber == 4){
      lcd.setCursor(15, 0);
      lcd.print("Electrons are delicious!");
      num_chars = strlen("Electrons are delicious!");
    }else if(randnumber == 5){
      lcd.setCursor(15, 0);
      lcd.print(":) <3");
      num_chars = strlen(":) <3");
    }else if(randnumber == 6){
      lcd.setCursor(15, 0);
      lcd.print("<3 <3 <3");
      num_chars = strlen("<3 <3 <3");
    }else if(randnumber == 7){
      lcd.setCursor(15, 0);
      lcd.print("Have a nice day! :)");
      num_chars = strlen("Have a nice day! :)");
    }else if(randnumber == 8){
      lcd.setCursor(15, 0);
      lcd.print("I like cats. Meow!");
      num_chars = strlen("I like cats. Meow!");
    }else if(randnumber == 9){
      lcd.setCursor(15, 0);
      lcd.print("Hi there! I'm Belle.");
      num_chars = strlen("Hi there! I'm Belle.");          
    }else if(randnumber == 10){
      lcd.setCursor(15, 0);
      lcd.print("Visit me @ iambelle.net!");
      num_chars = strlen("Visit me @ iambelle.net!");
    }else if(randnumber == 11){
      lcd.setCursor(15, 0);
      lcd.print("I love being nice!");
      num_chars = strlen("I love being nice!");
    }else if(randnumber == 12){
      lcd.setCursor(15, 0);
      lcd.print(":D :D :D");
      num_chars = strlen(":D :D :D");
    }
          
    // scroll until string moves offscreen left:
    if(num_chars > 0){
      for (int positionCounter = 0; positionCounter < num_chars + 15; positionCounter++) {
        // wait a bit:      
        delay(150);
        // scroll one position left:
        lcd.scrollDisplayLeft();
      }
    } 
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/

