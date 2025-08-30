-- # Class: Node
--     * Slot: iri
--     * Slot: label
--     * Slot: type
--     * Slot: source
--     * Slot: Graph_id Description: Autocreated FK slot
-- # Class: Edge
--     * Slot: id
--     * Slot: subject
--     * Slot: predicate
--     * Slot: object
--     * Slot: source
--     * Slot: gene_expr
--     * Slot: Graph_id Description: Autocreated FK slot
-- # Class: Graph
--     * Slot: id

CREATE TABLE "Graph" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Graph_id" ON "Graph" (id);
CREATE TABLE "Node" (
	iri TEXT NOT NULL,
	label TEXT NOT NULL,
	type TEXT NOT NULL,
	source TEXT NOT NULL,
	"Graph_id" INTEGER,
	PRIMARY KEY (iri),
	FOREIGN KEY("Graph_id") REFERENCES "Graph" (id)
);CREATE INDEX "ix_Node_iri" ON "Node" (iri);
CREATE TABLE "Edge" (
	id INTEGER NOT NULL,
	subject TEXT NOT NULL,
	predicate TEXT NOT NULL,
	object TEXT NOT NULL,
	source TEXT NOT NULL,
	gene_expr FLOAT,
	"Graph_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(subject) REFERENCES "Node" (iri),
	FOREIGN KEY(object) REFERENCES "Node" (iri),
	FOREIGN KEY("Graph_id") REFERENCES "Graph" (id)
);CREATE INDEX "ix_Edge_id" ON "Edge" (id);
