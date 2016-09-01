import java.util.Arrays;
import java.util.List;

public class Relations {
// P21 sex or gender
// P27 country of citizenship
// P22 father
// P25 mother
// P7 brother
// P9 sister
// P26 spouse
// P451 partner
// P40 child
// P43 stepfather
// P44 stepmother
// P1038 relative
// P1290 godparent

	public static final List<String> IMPORTANT_RELATIONS = Arrays.asList(
			"P527",	// has part
			"P6",	// head of government
			"P22",	// father
			"P495",	// country of origin
			"P37",	// official language
			"P463",	// member of
			"P20",	// place of death
			"P27",	// country of citizenship
			"P194",	// legislative body
			"P641",	// sport
			"P131",	// located in the administrative territorial entity
			"P1344",	// participant of
			"P364",	// original language of work
			"P103",	// native language
			"P40",	// child
			"P17",	// country
			"P1376",	// capital of
			"P35",	// head of state
			"P551",	// residence
			"P279",	// subclass of
			"P361",	// part of
			"P1589",	// deepest point
			"P26",	// spouse
			"P112",	// founder
			"P150",	// subdivides into
			"P530",	// diplomatic relation
			"P31",	// instance of
			"P123",	// publisher
			"P47",	// shares border with
			"P1441",	// present in work
			"P36",	// capital
			"P50",	// author
			"P800",	// notable work
			"P1412"	// languages spoken, written or signed
			);
}
