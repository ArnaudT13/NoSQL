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
			// Cr�ation du driver pour le cluster cassandra
		    cluster = Cluster.builder()
		    		.addContactPoint("127.0.0.1")
		    		.withPort(9042)
		            .build();
		    
		    // Cr�ation de la session correspondant au keyspace
		    Session session = cluster.connect("cycling"); 

		    // Ex�cution de la requ�te
		    ResultSet rs = session.execute("SELECT * FROM cyclists");
		    
		    // R�cup�ration et traitement du r�sultat
		    List<Row> rows = rs.all();
		    for (Row row : rows) {
			    System.out.println(row.toString());
		    }
		} finally {
		    if (cluster != null) cluster.close();
		}

	}

}
