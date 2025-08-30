
# Class: Edge



URI: [kg:Edge](https://purl.humanatlas.io/vocab/kg#Edge)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Node],[Node]<object%201..1-%20[Edge&#124;predicate:Uri;source:Uri;gene_expr:float%20%3F],[Node]<subject%201..1-%20[Edge],[Graph]++-%20edges%200..*>[Edge],[Graph])](https://yuml.me/diagram/nofunky;dir:TB/class/[Node],[Node]<object%201..1-%20[Edge&#124;predicate:Uri;source:Uri;gene_expr:float%20%3F],[Node]<subject%201..1-%20[Edge],[Graph]++-%20edges%200..*>[Edge],[Graph])

## Referenced by Class

 *  **None** *[➞edges](graph__edges.md)*  <sub>0..\*</sub>  **[Edge](Edge.md)**

## Attributes


### Own

 * [subject](subject.md)  <sub>1..1</sub>
     * Range: [Node](Node.md)
 * [predicate](predicate.md)  <sub>1..1</sub>
     * Range: [Uri](types/Uri.md)
 * [object](object.md)  <sub>1..1</sub>
     * Range: [Node](Node.md)
 * [source](source.md)  <sub>1..1</sub>
     * Range: [Uri](types/Uri.md)
     * Example: https://purl.humanatlas.io/vocab/hp None
 * [gene_expr](gene_expr.md)  <sub>0..1</sub>
     * Range: [Float](types/Float.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | rdf:Statement |
