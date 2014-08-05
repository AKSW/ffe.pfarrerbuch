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
      <xsl:apply-templates select="vicar"/>
    </rdf:RDF>
  </xsl:template>

  <!-- template for persons table -->
  <xsl:template match="vicar">
    <xsl:element name="foaf:Person">
      <xsl:attribute name="rdf:about">&person;<xsl:value-of select="id" /></xsl:attribute>
      <xsl:attribute name="rdfs:label"><xsl:value-of select="name" /></xsl:attribute>
      <xsl:attribute name="foaf:name"><xsl:value-of select="name" /></xsl:attribute>
      <!-- <xsl:attribute name="foaf:lastName"><xsl:value-of select="column[@name='Name']" /></xsl:attribute>-->
      <!-- <xsl:attribute name="foaf:firstName"><xsl:value-of select="column[@name='Vorname']" /></xsl:attribute>-->
      <!-- <xsl:attribute name="hp:nameVariant"><xsl:value-of select="column[@name='Namen_Varianten']" /></xsl:attribute>-->
      <!-- <xsl:attribute name="hp:birthName"><xsl:value-of select="column[@name='Geburtsname']" /></xsl:attribute>-->
      <xsl:attribute name="hp:birthDate"><xsl:value-of select="birthday/date" /></xsl:attribute>
      <xsl:attribute name="hp:dateOfOrdination"><xsl:value-of select="ordination/date" /></xsl:attribute>
      <xsl:attribute name="hp:dateOfDeath"><xsl:value-of select="obit/date" /></xsl:attribute>

      <xsl:attribute name="rdfs:comment"><xsl:value-of select="misc" /></xsl:attribute>
      <xsl:attribute name="rdfs:comment"><xsl:value-of select="literature" /></xsl:attribute>

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
      <xsl:if test="father">
          <xsl:call-template name="parent">
              <xsl:with-param name="child" select="id" />
              <xsl:with-param name="parent" select="father" />
              <xsl:with-param name="gender">male</xsl:with-param>
              <xsl:with-param name="property">hp:father</xsl:with-param>
          </xsl:call-template>
      </xsl:if>
      <xsl:if test="mother">
          <xsl:call-template name="parent">
              <xsl:with-param name="child" select="id" />
              <xsl:with-param name="parent" select="mother" />
              <xsl:with-param name="gender">female</xsl:with-param>
              <xsl:with-param name="property">hp:mother</xsl:with-param>
          </xsl:call-template>
      </xsl:if>

      <!-- Dates -->
      <!--//
      <xsl:call-template name="date">
        <xsl:with-param name="year" select="column[@name='Geburtsjahr']" />
        <xsl:with-param name="day" select="column[@name='Geburtstag']" />
        <xsl:with-param name="property">hp:birthDate</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="date">
        <xsl:with-param name="day" select="column[@name='Tauftag']" />
        <xsl:with-param name="property">hp:dayOfBaptism</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="date">
        <xsl:with-param name="year" select="column[@name='Ordinationsjahr']" />
        <xsl:with-param name="day" select="column[@name='Ordinationstag']" />
        <xsl:with-param name="property">hp:dateOfOrdination</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="date">
        <xsl:with-param name="year" select="column[@name='Emeritierungsjahr']" />
        <xsl:with-param name="day" select="column[@name='Emeritierungstag']" />
        <xsl:with-param name="property">hp:dateOfRetirement</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="date">
        <xsl:with-param name="year" select="column[@name='Todesjahr']" />
        <xsl:with-param name="day" select="column[@name='Todestag']" />
        <xsl:with-param name="property">hp:dateOfDeath</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="date">
        <xsl:with-param name="day" select="column[@name='Begraebnistag']" />
        <xsl:with-param name="property">hp:dayOfFuneral</xsl:with-param>
      </xsl:call-template>
      //-->

      <!-- Places -->
      <!--//
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Begraebnisort_Key']" />
        <xsl:with-param name="property">hp:burialPlace</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Emeritierungsort_Key']" />
        <xsl:with-param name="property">hp:placeOfRetirement</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Ordinationssort_Key']" />
        <xsl:with-param name="property">hp:placeOfOrdination</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Taufort_Key']" />
        <xsl:with-param name="property">hp:placeOfBaptism</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Todesort_Key']" />
        <xsl:with-param name="property">hp:placeOfDeath</xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="place">
        <xsl:with-param name="place" select="column[@name='Geburtsort_Key']" />
        <xsl:with-param name="property">hp:birthPlace</xsl:with-param>
      </xsl:call-template>
  //-->
    </xsl:element>
  </xsl:template>

  <!-- template for position table -->
  <xsl:template match="pastor">
    <xsl:element name="hp:Position">
    </xsl:element>
  </xsl:template>


  <xsl:template name="place">
    <xsl:param name="place"/>
    <xsl:param name="property"/>
    <xsl:if test="$place != ''">
        <xsl:element name="{$property}">
            <xsl:element name="rdf:Description">
                <xsl:attribute name="rdf:about">&place;<xsl:value-of select="$place"/></xsl:attribute>
            </xsl:element>
        </xsl:element>
    </xsl:if>
  </xsl:template>

  <xsl:template name="position">
    <xsl:param name="position"/>
    <xsl:element name="hp:hasPosition">
      <xsl:element name="rdf:Description">
        <xsl:attribute name="rdf:about">&position;<xsl:value-of select="$position"/></xsl:attribute>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template name="parent">
    <xsl:param name="child"/>
    <xsl:param name="parent"/>
    <xsl:param name="gender"/>
    <xsl:param name="property"/>
    <xsl:variable name="parent-uri">
        <xsl:call-template name="string-replace-all">
            <xsl:with-param name="text" select="$parent" />
            <xsl:with-param name="replace" select="' '" />
            <xsl:with-param name="by" select="''" />
        </xsl:call-template>
    </xsl:variable>
    <xsl:element name="{$property}">
      <xsl:element name="foaf:Person">
        <xsl:attribute name="rdf:about"><xsl:value-of select="$child"/>-<xsl:value-of select="$parent-uri"/></xsl:attribute>
        <xsl:attribute name="foaf:name"><xsl:value-of select="$parent"/></xsl:attribute>
        <xsl:attribute name="foaf:gender"><xsl:value-of select="$gender"/></xsl:attribute>
      </xsl:element>
    </xsl:element>
  </xsl:template>

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

</xsl:stylesheet>
