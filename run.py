from booking.booking import Booking
import time

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency()
        bot.select_place_to_go("New York")
        bot.select_dates(check_in_date="2025-03-25", check_out_date="2025-03-29")
        bot.select_adults(1)
        bot.cliclk_search()
        bot.apply_filtration()

except Exception as e:
    if 'in PATH' in str(e):
        print("There is a problem running this program.")
    else:
        raise

time.sleep(60)



