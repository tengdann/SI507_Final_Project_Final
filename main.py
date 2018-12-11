import database
import scraping
import testing
import visualization

prompt = '''Please choose from the following:\n
database
    Reinitializes the database/cache.\n
scraping
    Makes a call to the API and dynamically scrapes stories from BBC.\n
testing
    Runs a few unit tests to ensure the database is initialized properly and data is properly stored.\n
visualization
    Starts the Flask in a local environment, allowing for some data visualization.\n
quit
    Quit the program.
    
Make your selection now: '''

if __name__ == '__main__':
    user_input = input(prompt)
    
    while user_input.lower() != 'quit':
        if user_input.lower() == 'database':
            database.db_main()
        elif user_input.lower() == 'scraping':
            user_decision = input('Are you sure you want to scrape? This will take some time! (y/n): ')
            if user_decision.lower() == 'y':
                scraping.sc_main()
            else:
                pass
        elif user_input.lower() == 'testing':
            user_decision = input('Are you sure you want to test? This will take around 20 seconds, depending on hardware speed. (y/n): ')
            if user_decision.lower() == 'y':
                testing.te_main()
            else:
                pass
        elif user_input.lower() == 'visualization':
            visualization.vi_main()
        else:
            print('Invalid input, please try again!')
        
        print()
        user_input = input(prompt)