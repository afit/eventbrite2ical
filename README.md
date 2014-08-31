#eventbrite2ical#

##Description##

Python library to create an iCal feed from an EventBrite account on the fly.

For the latest updates, look at:

* [This project's home on GitHub](https://github.com/reincubate/eventbrite2ical/)

##Usage##

###Installation###

####Installation using pip####

    pip install git+https://github.com/reincubate/eventbrite2ical

Or, for just this version

    pip install git+https://github.com/reincubate/eventbrite2ical#eventbrite2ical==0.1

###Loading the eventbrite2ical code###

    from eventbrite2ical import eventbrite2ical

###Initializing the client###

You will need to pass authentication credentials through eventbrite2ical just as you do with the [eventbrite Python API](http://github.com/eventbrite/eventbrite-client-py/). Fuller examples are available there. The ID parameter in this instance reflects the ID of the organization to query in EventBrite.

    eb_auth_tokens = { 'app_key':  'YOUR_APP_KEY' }
    eb_list_args = { 'id': 0, 'event_statuses': 'live,started' }

    eb_feed = eventbrite2ical.fetch_eb_organizer_feed( eb_auth_tokens, eb_list_args )

    ical = eventbrite2ical.ical_from_eb_feed( eb_feed )

##Resources##
* iCalendar documentation - <https://github.com/collective/icalendar/blob/master/docs/usage.rst>
* EventBrite Python API source - <http://github.com/eventbrite/eventbrite-client-py/>
* EventBrite API documentation - <http://developer.eventbrite.com/doc/>