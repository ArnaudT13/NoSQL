package cassandra;

import java.sql.Timestamp;
import java.util.List;

import com.datastax.driver.core.*;
import com.datastax.driver.core.policies.DCAwareRoundRobinPolicy;
import com.datastax.driver.core.policies.TokenAwarePolicy;

/**
 * Class that represents a Weather Data from Weather Station with Cassandra.
 *
 * @author Arnaud TAVERNIER
 * @author C�dric GORMOND
 */
public class WeatherStation {

	public final static String KEYSPACE_NAME = "WeatherStation";
	public final static String TABLE_NAME = "weather";

	private static Cluster cluster = null;

	private static Session session = null;

	/**
	 * Connect to a Cassandra DB.
	 *
	 * @param ip 127.0.0.1 by default
	 * @param port 9042 by default
	 */
	public void connect(String ip, Integer port) {
		cluster = Cluster.builder()
				.addContactPoint(ip)
				.withPort(port)
				.withProtocolVersion(ProtocolVersion.V4)
				.build();

		session = cluster.connect();
	}

	public Session getSession() {
		return this.session;
	}

	/**
	 * Close connection to the Cassandra DB.
	 */
	public void close() {
		session.close();
		cluster.close();
	}

	/**
	 * Create a KEYSPACE from the given arguments
	 *
	 * @param keyspaceName
	 * @param replicationStrategy SimpleStrategy by default
	 * @param replicationFactor 1 by default
	 */
	public void createKeyspace(String keyspaceName, String replicationStrategy, int replicationFactor) {
		StringBuilder sb = new StringBuilder("CREATE KEYSPACE IF NOT EXISTS ")
						.append(keyspaceName).append(" WITH replication = {")
						.append("'class':'").append(replicationStrategy)
						.append("','replication_factor':").append(replicationFactor)
						.append("};");

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Delete the given keyspace.
	 *
	 * @param keyspaceName (string)
	 */
	public void deleteKeyspace(String keyspaceName) {
		StringBuilder sb = new StringBuilder("DROP KEYSPACE ").append(keyspaceName);

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Drop the given table
	 *
	 * @param tableName name of the table to drop
	 */
	public void dropTable(String tableName) {
		StringBuilder sb = new StringBuilder("DROP KEYSPACE ").append(tableName);

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Create a table (weather unit) with a given name.
	 *
	 * The PRIMARY KEY (idStation, time, id) represents XXXX
	 *
	 * @param tableName (string)
	 */
	public void createTable(String tableName) {
		StringBuilder sb = new StringBuilder("CREATE TABLE IF NOT EXISTS ")
				.append(tableName)
				.append("(")
				.append("id timeuuid,")
				.append("idStation bigint,")
				.append("longitude double,")
				.append("latitude double, ")
				.append("time timestamp, ")
				.append("temperature float,")
				.append("humidity float,")
				.append("pressure float,")
				.append("PRIMARY KEY (idStation, time, id) )");


		String query = sb.toString();
		session.execute(query);
	}


	/**
	 * Create an advanced weather table unit.
	 *
	 */
	public void createWeatherAdvancedTable() {
		StringBuilder sb = new StringBuilder("CREATE MATERIALIZED VIEW IF NOT EXISTS ")
				.append("weather_advanced")
				.append(" AS SELECT ")
				.append("id,")
				.append("idStation,")
				.append("longitude,")
				.append("latitude, ")
				.append("time, ")
				.append("temperature,")
				.append("humidity,")
				.append("pressure")
				.append(" FROM weather ")
				.append("WHERE time IS NOT NULL AND idStation IS NOT NULL PRIMARY KEY (idStation, time)")
				.append(";");

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Insert values into a given Table. The UUID is auto-generated by Cassandra thanks to now() function.
	 *
	 *
	 * @param tableName targeted table
	 * @param idStation Id station where the metrics come from
	 * @param longitude Longitude (double)
	 * @param latitude Latitude (double)
	 * @param time Timestamp (timestamp in seconds)
	 * @param temperature (float)
	 * @param humidity (float percentage between 0 and 100)
	 * @param pressure (pressure float in hPa)
	 */
	public void insertValue(String tableName, long idStation, double longitude, double latitude, Timestamp time, float temperature, float humidity, float pressure) {
		StringBuilder sb = new StringBuilder("INSERT INTO ")
				.append(tableName)
				.append(" (id, idStation, longitude, latitude, time, temperature, humidity, pressure)")
				.append("VALUES (")
				.append("now(), ") //Generate UUID with time aspect
				.append(idStation +", ")
				.append(longitude +", ")
				.append(latitude +", ")
				.append(time.getTime() +", ")
				.append(temperature +", ")
				.append(humidity +", ")
				.append(pressure)
				.append(");");

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Delete values of a row represented by an iD into a given Table.
	 *
	 *
	 * @param tableName targeted table
	 */
	public void deleteValue(String tableName, String id) {
		StringBuilder sb = new StringBuilder("DELETE FROM ")
				.append(tableName)
				.append("WHERE id = ")
				.append(id)
				.append(" IF EXISTS;");

		String query = sb.toString();
		session.execute(query);
	}

	/**
	 * Execute and display a given query.
	 *
	 * @param query to execute, i.e. "SELECT * FROM weather"
	 */
	public void executeAndDisplayQuery(String query){
		System.out.println(Utils.YELLOW + "\n[INFO] " + Utils.RESET + query );

		try {
			// Execute query into Cassandra
			ResultSet rs = session.execute(query);

			// Extraction of the previous result
			List<Row> rows = rs.all();
			for (Row row : rows) {
				System.out.println(row.toString());
			}

			if (rs.isExhausted()) {
				System.out.println(Utils.GREEN + "[INFO] " + Utils.RESET + "Done.");
			}else{
				System.out.println(Utils.RED + "[INFO] " + Utils.RESET + "Failed.");
			}

		} finally {
			if (cluster == null) cluster.close();
		}
	}

	public static void main(String[] args) {

		WeatherStation client = new WeatherStation();
		client.connect("127.0.0.1", 9042);
		session = client.getSession();

		// Delete keyspace for demo
		client.deleteKeyspace(KEYSPACE_NAME);

		// Create keyspace if it doesn't exist
		client.createKeyspace(KEYSPACE_NAME, "SimpleStrategy", 1);

		// Connect to the keyspace created above
		session = cluster.connect(KEYSPACE_NAME);

		// Create weather table
		client.createTable(TABLE_NAME);

		// Inserting values into weather
		client.insertValue(TABLE_NAME, 1, 4.43, 45.434, new Timestamp(1611742249200L), 1, 20, 1005);
		client.insertValue(TABLE_NAME, 1, 4.43, 45.434, new Timestamp(1611742249300L), -1, 18, 1000);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249400L), 5, 42, 864);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249500L), 6, 41, 834);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249600L), 6, 41, 846);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249700L), 5, 40, 850);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249800L), 4, 40, 841);
		client.insertValue(TABLE_NAME, 2, 6.53, 45.75, new Timestamp(1611742249900L), 5, 41, 836);

		// Queries
		client.executeAndDisplayQuery("SELECT * FROM weather");
		client.executeAndDisplayQuery("SELECT * FROM weather WHERE idStation = 1");
		client.executeAndDisplayQuery("SELECT * FROM weather WHERE idStation = 1"
				+ " AND time='"
				+ new Timestamp(1611742249300L).getTime() + "'");

		client.executeAndDisplayQuery("SELECT * FROM weather WHERE idStation = 2");
		client.executeAndDisplayQuery("SELECT * FROM weather WHERE idStation = 2"
				+ "  AND time >'"
				+ new Timestamp(1611742249500L).getTime()
				+ "' AND time <'"
				+ new Timestamp(1611742249800L).getTime()+ "'");

		client.close();
	}
}
