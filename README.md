# Ingredient_Tracker
a tool to help with alchemy in my (modded) skyrim sessions XD


THE PROBLEM:
  I play a modified version of Skyrim that's referred to as "WIldlander". 
  This mod pack contains a particular mod that introduces a mechanic that
  allows the player to both 1) breakdown alchemy ingredients into chemicals
  and 2) recombine chemicals into either difficult-to-obtain ingredients or new
  elixiers.

  However the mechanic doesn't keep track of which ingredients breakdown into what 
  chemicals-- It's up to the player to remember which ingredients yield what chemicals.


HOW TO USE THIS INGREDIENT TRACKER:
  1) Download the "Ingredient Tracker.exe" file and run it. It's located within the dist folder
  2) From there you can experiment with the tool. Select a CONTEXT button (find/+/-). These buttons define the context of the operation. "Find" displays all relevant data that matches your criteria to the output table.
     "+" either adds a new ingredient (if the ingredient doesn't exist) or it updates a matching ingredient with new data. You can both add new chemicals and update prexisting ones in the same operation.
     "-" removes data from the application. To remove an ingredient, submit its name only. Otherwise specifiy the ingredient along with the chemicals you wish to remove before submission. If there aren't enough
     chemical entry fields, you can adjust the number of entries by clicking the +/- buttons underneath the chemical section of the input fields.
  4) Once a context is selected, next specify the ingredient name and/or chemical data to better define the operation.
  5) Once you've specified your query, click the ">>" button to submit the operation.
  6) The "C" button clears the fields for quicker querying.
  7) You can also Import/Export data files to save/load your data! Just go to file > Import/Export.
  8) If you want to clear the database and start fresh, go to File > New


And that's it! This project took about a month to get up and running (had to learn the GUI stuff). The Utilities.py file is actually unsused-- take a peek at it if you're intereseted in seeing the UI implementation 
BEFORE the GUI existed. That's why I left it in ^_^
  
