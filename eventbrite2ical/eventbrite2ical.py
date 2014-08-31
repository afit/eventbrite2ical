from datetime import datetime
from icalendar import Calendar, Event, vCalAddress
from eventbrite import EventbriteClient
from pytz import timezone

def fetch_eb_organizer_feed( credentials, event_args ):
    ''' Pulls down a feed of events for an EventBrite organizer. '''
    eb_client = EventbriteClient( credentials )
    return eb_client.organizer_list_events( event_args )

def ical_from_eb_feed( eb_feed ):
    ''' Converts an EventBrite feed into iCal format. '''
    cal = Calendar()
    cal.add('prodid', '-//eventbrite2ical//reincubate//')
    cal.add('version', '2.0')

    for event in eb_feed['events']:
        tzinfo = timezone( event['event']['timezone'] )

        title = event['event']['title']
        description = event['event']['title']
        url = event['event']['url']

        organiser = event['event']['organizer']['name']
        venue = event['event']['venue']
        venue_address = ', '.join( [ venue['name'], venue['address'], venue['address_2'], venue['city'], venue['region'], venue['postal_code'], venue['country'], ] )
        latitude = venue['latitude']
        longitude = venue['longitude']

        start_date = datetime.strptime( event['event']['start_date'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
        end_date = datetime.strptime( event['event']['end_date'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
        created = datetime.strptime( event['event']['created'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
      
        entry = Event()
        entry.add( 'summary', title )
        entry.add( 'description', '\n\n'.join( [ description, url, ] ) )
        entry.add( 'dtstart', start_date )
        entry.add( 'dtend',  end_date )
        entry.add( 'dtstamp', created )
        entry.add( 'location', venue_address )
        entry.add( 'geoLat', latitude )
        entry.add( 'geoLong', longitude )

        eorganiser = vCalAddress( url )
        eorganiser.params['cn'] = organiser
        entry['organizer'] = eorganiser

        cal.add_component( entry )

    return cal.to_ical()