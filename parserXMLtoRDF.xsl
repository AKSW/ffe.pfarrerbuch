<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE rdf:RDF [
<!ENTITY attendingschool "http://pfarrerbuch.comiles.eu/ungarn/schulbesuch/">
<!ENTITY hp "http://purl.org/voc/hp/">
<!ENTITY pfarrer "http://pfarrerbuch.comiles.eu/">
<!ENTITY person "http://pfarrerbuch.comiles.eu/ungarn/person/">
<!ENTITY place "http://pfarrerbuch.comiles.eu/ungarn/ort/">
<!ENTITY position "http://pfarrerbuch.comiles.eu/ungarn/position/">
<!ENTITY school "http://pfarrerbuch.comiles.eu/ungarn/school/">
<!ENTITY staffing "http://pfarrerbuch.comiles.eu/ungarn/staffing/">
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
            <!-- attributes -->
            <xsl:apply-templates select="id" />
            <!--<xsl:attribute name="rdfs:label">Name und Lebensdaten</xsl:attribute>-->
            <xsl:apply-templates select="name" />
            <xsl:if test="birthday/date">
                <xsl:attribute name="hp:birthDate"><xsl:value-of select="birthday/date" /></xsl:attribute>
            </xsl:if>
            <xsl:if test="ordination/date">
                <xsl:attribute name="hp:dateOfOrdination"><xsl:value-of select="ordination/date" /></xsl:attribute>
            </xsl:if>
            <xsl:if test="obit/date">
                <xsl:attribute name="hp:dateOfDeath"><xsl:value-of select="obit/date" /></xsl:attribute>
            </xsl:if>

            <!-- elements -->
            <xsl:element name="hp:isPastor"><xsl:attribute name="rdf:datatype">&xsd;boolean</xsl:attribute>true</xsl:element>

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

            <xsl:apply-templates select="education" mode="property" /> <!-- St -->
            <xsl:apply-templates select="teacher" mode="property" /> <!-- LM -->
            <!-- V scheint nie angegeben zu sein -->
            <xsl:apply-templates select="pastor" mode="property" /> <!-- VDM -->
            <xsl:apply-templates select="institution" mode="property" /> <!-- S -->

            <xsl:if test="misc">
                <xsl:element name="rdfs:comment"><xsl:value-of select="misc" /></xsl:element>
            </xsl:if>
            <xsl:if test="literature">
                <xsl:element name="rdfs:comment"><xsl:value-of select="literature" /></xsl:element>
            </xsl:if>
        </xsl:element>
        <!-- end of foaf:Person -->

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
        <xsl:attribute name="foaf:name"><xsl:value-of select="." /></xsl:attribute>
        <!-- <xsl:attribute name="foaf:lastName"><xsl:value-of select="column[@name='Name']" /></xsl:attribute>-->
        <!-- <xsl:attribute name="foaf:firstName"><xsl:value-of select="column[@name='Vorname']" /></xsl:attribute>-->
        <!-- <xsl:attribute name="hp:nameVariant"><xsl:value-of select="column[@name='Namen_Varianten']" /></xsl:attribute>-->
        <!-- <xsl:attribute name="hp:birthName"><xsl:value-of select="column[@name='Geburtsname']" /></xsl:attribute>-->
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
        <xsl:variable name="placeUri">
            <xsl:call-template name="placeUri">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="hp:attendedSchool">
            <xsl:element name="rdf:Description">
                <xsl:attribute name="rdf:about"><xsl:value-of select="$placeUri"/></xsl:attribute>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <xsl:template match="pastor|teacher|institution" mode="property">
        <xsl:variable name="placeUri">
            <xsl:call-template name="placeUri">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="hp:hasPosition">
            <xsl:element name="rdf:Description">
                <xsl:attribute name="rdf:about"><xsl:value-of select="$placeUri"/></xsl:attribute>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <xsl:template match="education" mode="reification">
        <xsl:param name="person"/>
        <xsl:variable name="placeUriName">
            <xsl:call-template name="placeUriName">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="placeUri">
            <xsl:call-template name="placeUri">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="hp:Event">
            <xsl:attribute name="rdf:about">&attendingschool;<xsl:value-of select="$placeUriName"/></xsl:attribute>
            <xsl:element name="rdf:subject"><xsl:value-of select="$person"/></xsl:element>
            <xsl:element name="rdf:predicate">hp:attendedSchool</xsl:element>
            <xsl:element name="rdf:object"><xsl:value-of select="$placeUri"/></xsl:element>
            <!--//
            <xsl:element name="hp:start"><xsl:value-of select="start"/></xsl:element>
            <xsl:element name="hp:end"><xsl:value-of select="end"/></xsl:element>
            //-->
            <!-- TODO -->
        </xsl:element>
    </xsl:template>

    <xsl:template match="pastor|teacher|institution" mode="reification">
        <xsl:param name="person"/>
        <xsl:variable name="placeUriName">
            <xsl:call-template name="placeUriName">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="placeUri">
            <xsl:call-template name="placeUri">
                <xsl:with-param name="place" select="." />
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="hp:Event">
            <xsl:attribute name="rdf:about">&staffing;<xsl:value-of select="$placeUriName"/></xsl:attribute>
            <xsl:element name="rdf:subject"><xsl:value-of select="$person"/></xsl:element>
            <xsl:element name="rdf:predicate">hp:hasPosition</xsl:element>
            <xsl:element name="rdf:object"><xsl:value-of select="$placeUri"/></xsl:element>
            <!--//
            <xsl:element name="hp:start"><xsl:value-of select="start"/></xsl:element>
            <xsl:element name="hp:end"><xsl:value-of select="end"/></xsl:element>
            //-->
            <!-- TODO -->
        </xsl:element>
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

    <!-- Helper templates -->
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

    <xsl:template name="placeUri">
        <xsl:param name="place" />
        <xsl:text>&place;</xsl:text>
        <xsl:call-template name="placeUriName">
            <xsl:with-param name="place" select="$place" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="placeUriName">
        <xsl:param name="place" />
        <xsl:variable name="placeNoSpace">
            <xsl:call-template name="string-replace-all">
                <xsl:with-param name="text" select="$place" />
                <xsl:with-param name="replace" select="' '" />
                <xsl:with-param name="by" select="''" />
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="$placeNoSpace" />
            <xsl:with-param name="replace" select="'/'" />
            <xsl:with-param name="by" select="'_'" />
        </xsl:call-template>
    </xsl:template>

</xsl:stylesheet>
