from typing import List
import psycopg2
import io


class QueryEngine:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        """Init QueryEngine's instance and create DSN rule for future connection

        Args:
            dbname (str): name of database to which Engine should connect
            user (str): user name to connect
            password (str): user's password
            host (str): database IP address
            port (str): database PORT
        """
        
        self.__DSN = f"dbname={dbname} user={user} password={password} host={host} port={port}"
        
    
    def get_products_info(self, classes: List) -> List[dict]:
        """This function are using to get info about products, which correspond to specified classes

        Args:
            classes (List): specified classes which are using to finding correspond products

        Returns:
            List[dict]: list of products info, each dictionary are responding to one product and contains next fields: name, image, price and discount
        """
        
        query_classes = [f"'{_}'" for _ in classes]
        select_query = F'''SELECT smart_scales_data.Products.name,
        smart_scales_data.Products.image,
        smart_scales_data.Products.price,
        smart_scales_data.Products.discount
        FROM (SELECT *
            FROM smart_scales_data.Classes
            WHERE class IN ({" ,".join(query_classes)})) AS names
        JOIN smart_scales_data.Products ON names.name = smart_scales_data.Products.name
        '''
        
        with psycopg2.connect(self.__DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(select_query)
                response = cur.fetchall()
        
        result = list()
        
        for row in response:
            d = {
                'name' : row[0],
                'image' : row[1].tobytes(),
                'price' : float(row[2]),
                'discount' : float(row[3])
            }
            result.append(d)
        
        return result