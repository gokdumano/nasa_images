import itertools
import requests
import typing
import time

class Images:
    @staticmethod
    def Search(
        q                : typing.Optional[str] = None, # Free text search terms to compare to all indexed metadata.
        center           : typing.Optional[str] = None, # NASA center which published the media.
        description      : typing.Optional[str] = None, # Terms to search for in `Description` fields.
        description_508  : typing.Optional[str] = None, # Terms to search for in `508 Description` fields.
        keywords         : typing.Optional[str] = None, # Terms to search for in `Keywords` fields. Separate multiple values with commas.
        location         : typing.Optional[str] = None, # Terms to search for in `Location` fields.
        media_type       : typing.Optional[str] = None, # Media types to restrict the search to. Available types: [`image`, `video`, `audio`]. Separate multiple values with commas.
        nasa_id          : typing.Optional[str] = None, # The media asset’s NASA ID.
        photographer     : typing.Optional[str] = None, # The primary photographer’s name.
        secondary_creator: typing.Optional[str] = None, # A secondary photographer/videographer’s name.
        title            : typing.Optional[str] = None, # Terms to search for in `Title` fields.
        year_start       : typing.Optional[str] = None, # The start year for results. Format: YYYY.
        year_end         : typing.Optional[str] = None  # The end year for results. Format: YYYY.
        ):
        """ Performing a search """
        with requests.Session() as s:
            url = 'https://images-api.nasa.gov/search'
            page_size = 100
            params = {
                'q'                : q,
                'center'           : center,
                'description'      : description,
                'description_508'  : description_508,
                'keywords'         : keywords,
                'location'         : location,
                'media_type'       : media_type,
                'nasa_id'          : nasa_id,
                'page_size'        : page_size,
                'photographer'     : photographer,
                'secondary_creator': secondary_creator,
                'title'            : title,
                'year_start'       : year_start,
                'year_end'         : year_end
                }
            items = []
            for page in range(1, 101):
                time.sleep(1)
                params.update({'page':page})
                r = s.get(url, params=params)
                
                try   : r.raise_for_status()
                except: return r.json().get('reason')

                collection  = r.json().get('collection')
                total_hits  = collection.get('metadata').get('total_hits')
                item        = collection.get('items')
                
                for it in item:
                    data, = it.get('data')
                    href  = it.get('href')
                    data.update({'href': href})
                    items.append(data)
                    
                print(f'Extracting items @ Page.{page:03d}... {len(items)/total_hits:7.2%}')
                if len(item) < page_size: break
                    
            return items
        
    @staticmethod
    def Asset(
        nasa_id: str # The media asset’s NASA ID.
        ):
        """ Retrieving a media asset’s manifest """
        with requests.Session() as s:
            url = f'https://images-api.nasa.gov/asset/{nasa_id}'
            r = s.get(url)
            
            try   : r.raise_for_status()
            except: return r.json().get('reason')
            
            items = r.json().get('collection').get('items')
            return items
        
    @staticmethod
    def Metadata(
        nasa_id: str # The media asset’s NASA ID.
        ):
        """ Retrieving a media asset’s metadata location """
        with requests.Session() as s:
            url = f'https://images-api.nasa.gov/metadata/{nasa_id}'
            r = s.get(url)
            
            try   : r.raise_for_status()
            except: return r.json().get('reason')
            
            location = r.json().get('location')
            return location
        
    @staticmethod
    def Captions(
        nasa_id: str # The media asset’s NASA ID.
        ):
        """ Retrieving a media asset’s metadata location """
        with requests.Session() as s:
            url = f'https://images-api.nasa.gov/captions/{nasa_id}'
            r = s.get(url)
            
            try   : r.raise_for_status()
            except: return r.json().get('reason')
            
            location = r.json().get('location')
            return location
        
    @staticmethod
    def Album(
        album_name: str # The media album’s name (case-sensitive).
        ):
        """ Retrieving a media album’s contents """
        with requests.Session() as s:
            url = f' https://images-api.nasa.gov/album/{album_name}'
            items = []
            for page in range(1, 101):
                time.sleep(1)
                r = s.get(url, params={'page':page,'page_size':50})
                
                try   : r.raise_for_status()
                except: return r.json().get('reason')

                collection  = r.json().get('collection')
                total_hits  = collection.get('metadata').get('total_hits')
                item        = collection.get('items')
                
                for it in item:
                    data, = it.get('data')
                    href  = it.get('href')
                    data.update({'href': href})
                    data.pop('album')
                    items.append(data)
                    
                print(f'Extracting items @ Page.{page:03d}... {len(items)/total_hits:7.2%}')
                if len(item) < 50: break
                    
            return items

if __name__ == '__main__':
    search   = Images.Search('Uranus')
    asset    = Images.Asset('PIA01535')
    metadata = Images.Metadata('PIA01535')
    captions = Images.Captions('PIA01535')
    album    = Images.Album('Mars')



