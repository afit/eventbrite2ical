from datetime import datetime
from icalendar import Calendar, Event, vCalAddress
from eventbrite import EventbriteClient
from pytz import timezone

def fetch_eb_organizer_feed( credentials, event_args ):
    ''' Pulls down a feed of events for an EventBrite organizer. '''
    eb_client = EventbriteClient( credentials )
    return eb_client.organizer_list_events( event_args )

def ical_from_eb_feed( eb_feed, ignore_draft=True ):
    ''' Converts an EventBrite feed into iCal format. '''
    cal = Calendar()
    cal.add('prodid', '-//eventbrite2ical//reincubate//')
    cal.add('version', '2.0')

    for event in eb_feed['events']:
        if ignore_draft and event['event']['status'] == 'Draft':
            continue

        tzinfo = timezone( event['event']['timezone'] )

        title = event['event']['title']
        description = event['event']['title']
        url = event['event']['url']

        organiser = event['event']['organizer']['name']

        if not 'venue' in event['event']:
            venue = None
        else:
            venue = event['event']['venue']

            addresses = [ venue['name'], venue['address'], venue['address_2'], venue['city'], venue['region'], venue['postal_code'], venue['country'], ]
            filled_addresses = []
            for a in addresses:
                if a: filled_addresses.append( a )

            venue_address = ', '.join( filled_addresses )
            latitude = venue['latitude']
            longitude = venue['longitude']

        start_date = datetime.strptime( event['event']['start_date'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
        end_date = datetime.strptime( event['event']['end_date'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
        created = datetime.strptime( event['event']['created'], '%Y-%m-%d %H:%M:%S' ).replace(tzinfo=tzinfo)
      
        entry = Event()
        entry.add( 'summary', title )

        if url:
            description = '%s\n\n%s' % ( description, url )

        entry.add( 'description', description )
        entry.add( 'dtstart', start_date )
        entry.add( 'dtend',  end_date )
        entry.add( 'dtstamp', created )

        if venue:
            entry.add( 'location', venue_address )
            entry.add( 'geoLat', latitude )
            entry.add( 'geoLong', longitude )

        eorganiser = vCalAddress( url )
        eorganiser.params['cn'] = organiser
        entry['organizer'] = eorganiser

        cal.add_component( entry )

    return cal.to_ical()
