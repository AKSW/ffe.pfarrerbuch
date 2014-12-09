<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE rdf:RDF [
<!ENTITY attendingschool "http://pfarrerbuch.comiles.eu/ungarn/schulbesuch/">
<!ENTITY hp "http://purl.org/voc/hp/">
<!ENTITY pfarrer "http://pfarrerbuch.comiles.eu/">
<!ENTITY person "http://pfarrerbuch.comiles.eu/ungarn/person/">
<!ENTITY place "http://pfarrerbuch.comiles.eu/ungarn/ort/">
<!ENTITY position "http://pfarrerbuch.comiles.eu/ungarn/stelle/">
<!ENTITY school "http://pfarrerbuch.comiles.eu/ungarn/schule/">
<!ENTITY staffing "http://pfarrerbuch.comiles.eu/ungarn/stellenbesetzung/">
<!ENTITY foaf "http://xmlns.com/foaf/0.1/">
<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#">
<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">
<!ENTITY xsl "http://www.w3.org/1999/XSL/Transform">
<!ENTITY str "http://exslt.org/strings">
]>
<xsl:stylesheet
    xmlns:xsl="&xsl;"
    xmlns:hp="&hp;"
    xmlns:rdf="&rdf;"
    xmlns:rdfs="&rdfs;"
    xmlns:xsd="&xsd;"
    xmlns:str="&str;"
    xmlns:foaf="&foaf;"
    version="1.0"
    >
    <xsl:output method="xml" indent="yes" encoding="utf-8"/>

    <xsl:template match="/file">
        <rdf:RDF
            xml:base="&pfarrer;"
            xmlns:hp="&hp;"
            xmlns:rdf="&rdf;"
            xmlns:rdfs="&rdfs;"
            xmlns:foaf="&foaf;"
            xmlns:attendingschool="&attendingschool;"
            xmlns:person="&person;"
            xmlns:place="&place;"
            xmlns:position="&position;"
            xmlns:school="&school;"
            xmlns:xsd="&xsd;"
            xmlns:staffing="&staffing;"
            >
            <xsl:apply-templates select="vicar" />
        </rdf:RDF>
    </xsl:template>

    <!-- template for persons table -->
    <xsl:template match="vicar">
        <xsl:element name="foaf:Person">
            <!-- Anmerkung: es gibt keine Tauf-, Emeritierungs- und Begräbnisangaben -->
            <!-- Attributes -->
            <xsl:apply-templates select="id" />
            <!--<xsl:attribute name="rdfs:label">Name und Lebensdaten</xsl:attribute>-->

            <!-- Elements -->
            <xsl:apply-templates select="name" />
            <xsl:element name="hp:isPastor"><xsl:attribute name="rdf:datatype">&xsd;boolean</xsl:attribute>true</xsl:element>

            <!-- Dates -->
            <xsl:call-template name="date">
                <xsl:with-param name="date" select="birthday/date" />
                <xsl:with-param name="datatype" select="birthday/date/@datatype" />
                <xsl:with-param name="property">hp:birthDate</xsl:with-param>
            </xsl:call-template>

            <xsl:call-template name="date">
                <xsl:with-param name="date" select="ordination/date" />
                <xsl:with-param name="datatype" select="ordination/date/@datatype" />
                <xsl:with-param name="property">hp:dateOfOrdination</xsl:with-param>
            </xsl:call-template>

            <xsl:call-template name="date">
                <xsl:with-param name="date" select="obit/date" />
                <xsl:with-param name="datatype" select="obit/date/@datatype" />
                <xsl:with-param name="property">hp:dateOfDeath</xsl:with-param>
            </xsl:call-template>

            <!-- Places -->
            <xsl:call-template name="place">
                <xsl:with-param name="place" select="birthday/place" />
                <xsl:with-param name="property">hp:birthPlace</xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="place">
                <xsl:with-param name="place" select="ordination/place" />
                <xsl:with-param name="property">hp:placeOfOrdination</xsl:with-param>
            </xsl:call-template>
            <xsl:call-template name="place">
                <xsl:with-param name="place" select="obit/place" />
                <xsl:with-param name="property">hp:placeOfDeath</xsl:with-param>
            </xsl:call-template>

            <!-- Parents -->
            <xsl:apply-templates select="father">
                <xsl:with-param name="child" select="id" />
                <xsl:with-param name="gender">male</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="mother">
                <xsl:with-param name="child" select="id" />
                <xsl:with-param name="gender">female</xsl:with-param>
            </xsl:apply-templates>

            <!-- Education and Staffing -->
            <xsl:apply-templates select="education" mode="property" /> <!-- St -->
            <xsl:apply-templates select="teacher" mode="property" /> <!-- LM -->
            <!-- V scheint nie angegeben zu sein -->
            <xsl:apply-templates select="pastor" mode="property" /> <!-- VDM -->
            <xsl:apply-templates select="institution" mode="property" /> <!-- S -->

            <!-- Other -->
            <xsl:if test="misc">
                <xsl:element name="rdfs:comment"><xsl:value-of select="misc" /></xsl:element>
            </xsl:if>
            <xsl:if test="literature">
                <xsl:element name="hp:source"><xsl:value-of select="literature" /></xsl:element>
            </xsl:if>
        </xsl:element>
        <!-- end of foaf:Person -->

        <!-- Reification Resources -->
        <xsl:apply-templates select="education" mode="reification"> <!-- St -->
            <xsl:with-param name="person">&person;<xsl:value-of select="id" /></xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="teacher" mode="reification"> <!-- LM -->
            <xsl:with-param name="person">&person;<xsl:value-of select="id" /></xsl:with-param>
        </xsl:apply-templates>
        <!-- V scheint nie angegeben zu sein -->
        <xsl:apply-templates select="pastor" mode="reification"> <!-- VDM -->
            <xsl:with-param name="person">&person;<xsl:value-of select="id" /></xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="institution" mode="reification"> <!-- S -->
            <xsl:with-param name="person">&person;<xsl:value-of select="id" /></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="id">
        <xsl:attribute name="rdf:about">&person;<xsl:value-of select="." /></xsl:attribute>
    </xsl:template>

    <xsl:template match="name">
        <xsl:element name="foaf:name">
            <xsl:if test="surname != '0'">
                <xsl:value-of select="surname" />
            </xsl:if>
            <xsl:text>, </xsl:text>
            <xsl:if test="forename != '0'">
                <xsl:value-of select="forename" />
            </xsl:if>
        </xsl:element>
        <xsl:apply-templates select="surname">
            <xsl:with-param name="property">foaf:lastName</xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="forename">
            <xsl:with-param name="property">foaf:firstName</xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="surnameVariation">
            <xsl:with-param name="property">hp:lastNameVariant</xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="forenameVariation">
            <xsl:with-param name="property">hp:firstNameVariant</xsl:with-param>
        </xsl:apply-templates>
        <!--<xsl:element name="hp:birthName"><xsl:value-of select="column[@name='Geburtsname']" /></xsl:element>-->
    </xsl:template>

    <xsl:template match="surname|forename|surnameVariation|forenameVariation">
        <xsl:param name="property"/>
        <xsl:element name="{$property}">
            <xsl:if test=". != '0'">
                <xsl:value-of select="." />
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <!--//
        The modes "property" and "reification" are used for the nodes "education", "pastor", "teacher" and "institution".
        They were introduced to distinugish between the creation of the plain property and the reification resources.
        e.g.
            ex:person hp:hasPosition ex:position .
        is created in the mode "property" while
            ex:reificationNode a hp:Event ;
                               rdf:subject ex:person ;
                               rdf:predicate ex:hasPosition ;
                               rdf:object ex:position ;
                               hp:start "" ;
                               hp:end "" .
        is created int he mode "reification".
    //-->

    <xsl:template match="education" mode="property">
        <xsl:variable name="schoolUri">
            <xsl:call-template name="schoolUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="objectProperty">
            <xsl:with-param name="type">hp:School</xsl:with-param>
            <xsl:with-param name="predicate">hp:attendedSchool</xsl:with-param>
            <xsl:with-param name="objectUri" select="$schoolUri" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="teacher" mode="property">
        <xsl:variable name="schoolUri">
            <xsl:call-template name="schoolUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="objectProperty">
            <xsl:with-param name="type">hp:School</xsl:with-param>
            <xsl:with-param name="predicate">hp:hasPosition</xsl:with-param>
            <xsl:with-param name="objectUri" select="$schoolUri" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="pastor|institution" mode="property">
        <xsl:variable name="positionUri">
            <xsl:call-template name="positionUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="objectProperty">
            <xsl:with-param name="type">hp:Position</xsl:with-param>
            <xsl:with-param name="predicate">hp:hasPosition</xsl:with-param>
            <xsl:with-param name="objectUri" select="$positionUri" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="education" mode="reification">
        <xsl:param name="person"/>
        <xsl:variable name="schoolUri">
            <xsl:call-template name="schoolUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="event">
            <xsl:with-param name="eventUri">&attendingschool;<xsl:value-of select="@id"/></xsl:with-param>
            <xsl:with-param name="subjectUri" select="$person" />
            <xsl:with-param name="predicateUri">&hp;attendedSchool</xsl:with-param>
            <xsl:with-param name="objectUri" select="$schoolUri" />
            <xsl:with-param name="date" select="date"/>
            <xsl:with-param name="label"><xsl:value-of select="name"/> (<xsl:value-of select="date"/>)</xsl:with-param>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="teacher" mode="reification">
        <xsl:param name="person"/>
        <xsl:variable name="schoolUri">
            <xsl:call-template name="schoolUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="event">
            <xsl:with-param name="eventUri">&staffing;<xsl:value-of select="@id"/></xsl:with-param>
            <xsl:with-param name="subjectUri" select="$person" />
            <xsl:with-param name="predicateUri">&hp;hasPosition</xsl:with-param>
            <xsl:with-param name="objectUri" select="$schoolUri" />
            <xsl:with-param name="date" select="date"/>
            <xsl:with-param name="label"><xsl:value-of select="name"/> (<xsl:value-of select="date"/>)</xsl:with-param>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="pastor|institution" mode="reification">
        <xsl:param name="person"/>
        <xsl:variable name="positionUri">
            <xsl:call-template name="positionUri">
                <xsl:with-param name="place" select="name" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="event">
            <xsl:with-param name="eventUri">&staffing;<xsl:value-of select="@id"/></xsl:with-param>
            <xsl:with-param name="subjectUri" select="$person" />
            <xsl:with-param name="predicateUri">&hp;hasPosition</xsl:with-param>
            <xsl:with-param name="objectUri" select="$positionUri" />
            <xsl:with-param name="date" select="date"/>
            <xsl:with-param name="label"><xsl:value-of select="name"/> (<xsl:value-of select="date"/>)</xsl:with-param>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="father|mother">
        <xsl:param name="child"/>
        <xsl:param name="gender"/>
        <xsl:call-template name="parent">
            <xsl:with-param name="child" select="$child" />
            <xsl:with-param name="parent" select="." />
            <xsl:with-param name="gender" select="$gender" />
        </xsl:call-template>
    </xsl:template>

    <!-- Specific Helper Templates -->
    <xsl:template name="parent">
        <xsl:param name="child"/>
        <xsl:param name="parent"/>
        <xsl:param name="gender"/>
        <xsl:variable name="property">
            <xsl:choose>
                <xsl:when test="$gender = 'female'">hp:mother</xsl:when>
                <xsl:otherwise>hp:father</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="parent-uri">
            <xsl:call-template name="string-replace-all">
                <xsl:with-param name="text" select="$parent" />
                <xsl:with-param name="replace" select="' '" />
                <xsl:with-param name="by" select="''" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="{$property}">
            <xsl:element name="foaf:Person">
                <xsl:attribute name="rdf:about">&person;<xsl:value-of select="$child"/>-<xsl:value-of select="$parent-uri"/></xsl:attribute>
                <xsl:attribute name="foaf:name"><xsl:value-of select="$parent"/></xsl:attribute>
                <xsl:attribute name="foaf:gender"><xsl:value-of select="$gender"/></xsl:attribute>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <xsl:template name="place">
        <xsl:param name="place"/>
        <xsl:param name="property"/>
        <xsl:if test="$place != ''">
            <xsl:element name="{$property}">
                <xsl:element name="rdf:Description">
                    <xsl:attribute name="rdf:about">
                        <xsl:call-template name="placeUri">
                            <xsl:with-param name="place" select="$place" />
                        </xsl:call-template>
                    </xsl:attribute>
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <xsl:template name="event">
        <xsl:param name="eventUri"/>
        <xsl:param name="subjectUri"/>
        <xsl:param name="predicateUri"/>
        <xsl:param name="objectUri"/>
        <xsl:param name="date"/>
        <xsl:param name="label"/>
        <xsl:element name="hp:Event">
            <xsl:attribute name="rdf:about"><xsl:value-of select="$eventUri"/></xsl:attribute>
            <xsl:call-template name="objectProperty">
                <xsl:with-param name="predicate">rdf:subject</xsl:with-param>
                <xsl:with-param name="objectUri" select="$subjectUri" />
            </xsl:call-template>
            <xsl:call-template name="objectProperty">
                <xsl:with-param name="predicate">rdf:predicate</xsl:with-param>
                <xsl:with-param name="objectUri" select="$predicateUri" />
            </xsl:call-template>
            <xsl:call-template name="objectProperty">
                <xsl:with-param name="predicate">rdf:object</xsl:with-param>
                <xsl:with-param name="objectUri" select="$objectUri" />
            </xsl:call-template>
            <xsl:if test="str:tokenize($date,'-')[1] != ''">
                <xsl:element name="hp:start"><xsl:attribute name="rdf:datatype">&xsd;gYear</xsl:attribute><xsl:value-of select="str:tokenize($date,'-')[1]"/></xsl:element>
            </xsl:if>
            <xsl:if test="str:tokenize($date,'-')[2] != ''">
                <xsl:element name="hp:end"><xsl:attribute name="rdf:datatype">&xsd;gYear</xsl:attribute><xsl:value-of select="str:tokenize($date,'-')[2]"/></xsl:element>
            </xsl:if>
            <xsl:if test="$label != ''">
                <xsl:element name="rdfs:label"><xsl:value-of select="$label"/></xsl:element>
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <xsl:template name="placeUri">
        <xsl:param name="place" />
        <xsl:text>&place;</xsl:text>
        <xsl:call-template name="uriName">
            <xsl:with-param name="name" select="$place" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="schoolUri">
        <xsl:param name="place" />
        <xsl:text>&school;</xsl:text>
        <xsl:call-template name="uriName">
            <xsl:with-param name="name" select="$place" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="positionUri">
        <xsl:param name="place" />
        <xsl:text>&position;</xsl:text>
        <xsl:call-template name="uriName">
            <xsl:with-param name="name" select="$place" />
        </xsl:call-template>
    </xsl:template>

    <!-- Generic Helper Templates -->
    <xsl:template name="string-replace-all">
        <xsl:param name="text" />
        <xsl:param name="replace" />
        <xsl:param name="by" />
        <xsl:choose>
            <xsl:when test="contains($text, $replace)">
                <xsl:value-of select="substring-before($text,$replace)" />
                <xsl:value-of select="$by" />
                <xsl:call-template name="string-replace-all">
                    <xsl:with-param name="text" select="substring-after($text,$replace)" />
                    <xsl:with-param name="replace" select="$replace" />
                    <xsl:with-param name="by" select="$by" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="uriName">
        <xsl:param name="name" />
        <xsl:variable name="noSpace">
            <xsl:call-template name="string-replace-all">
                <xsl:with-param name="text" select="$name" />
                <xsl:with-param name="replace" select="' '" />
                <xsl:with-param name="by" select="''" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="$noSpace" />
            <xsl:with-param name="replace" select="'/'" />
            <xsl:with-param name="by" select="'_'" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="objectProperty">
        <xsl:param name="type"/>
        <xsl:param name="predicate"/>
        <xsl:param name="objectUri"/>
        <xsl:element name="{$predicate}">
            <xsl:variable name="elementName">
                <xsl:choose>
                    <xsl:when test="$type">
                        <xsl:value-of select="$type"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>rdf:Description</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:element name="{$elementName}">
                <xsl:attribute name="rdf:about"><xsl:value-of select="$objectUri"/></xsl:attribute>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <xsl:template name="date">
        <xsl:param name="date"/>
        <xsl:param name="datatype"/>
        <!-- inaccuracy -->
        <xsl:param name="property"/>
        <xsl:if test="$date != ''">
            <xsl:element name="{$property}">
                <xsl:if test="$datatype != ''">
                    <xsl:attribute name="rdf:datatype">&xsd;<xsl:value-of select="$datatype"/></xsl:attribute>
                </xsl:if>
                <xsl:value-of select="$date"/>
            </xsl:element>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
