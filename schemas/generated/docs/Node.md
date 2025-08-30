
# Class: Node



URI: [kg:Node](https://purl.humanatlas.io/vocab/kg#Node)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Graph]++-%20nodes%200..*>[Node&#124;iri:Uri;label:string;type:Uri;source:Uri],[Edge]-%20object%201..1>[Node],[Edge]-%20subject%201..1>[Node],[Graph],[Edge])](https://yuml.me/diagram/nofunky;dir:TB/class/[Graph]++-%20nodes%200..*>[Node&#124;iri:Uri;label:string;type:Uri;source:Uri],[Edge]-%20object%201..1>[Node],[Edge]-%20subject%201..1>[Node],[Graph],[Edge])

## Referenced by Class

 *  **None** *[➞nodes](graph__nodes.md)*  <sub>0..\*</sub>  **[Node](Node.md)**
 *  **None** *[object](object.md)*  <sub>1..1</sub>  **[Node](Node.md)**
 *  **None** *[subject](subject.md)*  <sub>1..1</sub>  **[Node](Node.md)**

## Attributes


### Own

 * [iri](iri.md)  <sub>1..1</sub>
     * Range: [Uri](types/Uri.md)
     * Example: http://purl.obolibrary.org/obo/UBERON_0014885 None
 * [label](label.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
     * Example: distal epiphysis of distal phalanx of manual digit 5 None
 * [type](type.md)  <sub>1..1</sub>
     * Range: [Uri](types/Uri.md)
     * Example: http://purl.obolibrary.org/obo/UBERON_0000061 None
 * [source](source.md)  <sub>1..1</sub>
     * Range: [Uri](types/Uri.md)
     * Example: https://purl.humanatlas.io/vocab/hp None

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | owl:Class |
