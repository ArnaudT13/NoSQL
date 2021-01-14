package cassandra;

import java.util.List;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;

public class WeatherStation {

	public static void main(String[] args) {
		
		Cluster cluster = null;
		try {
			// Création du driver pour le cluster cassandra
		    cluster = Cluster.builder()
		    		.addContactPoint("127.0.0.1")
		    		.withPort(9042)
		            .build();
		    
		    // Création de la session correspondant au keyspace
		    Session session = cluster.connect("cycling"); 

		    // Exécution de la requête
		    ResultSet rs = session.execute("SELECT * FROM cyclists");
		    
		    // Récupération et traitement du résultat
		    List<Row> rows = rs.all();
		    for (Row row : rows) {
			    System.out.println(row.toString());
		    }
		} finally {
		    if (cluster != null) cluster.close();
		}

	}

}
