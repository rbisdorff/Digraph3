<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- rubisOutrankingDigraph.xsl version 1.0-4 RB August 2007 -->

<xsl:template match="rubisOutrankingDigraph">
 <html>
  <head><title>D2-Decision-Deck UMCDA-ML application</title></head>
  <body>
   <h2>Rubis Outranking Digraph XML to HTML file converter</h2>
   <xsl:apply-templates/>
   <p>RB, December 2007, version 1.0-5</p>
   </body>
  </html>
</xsl:template>

<xsl:template match="header">
   <h1><font color="#0000bb">XML stored rubisOutrankingDigraph instance</font></h1>
   <table cellpadding="3">
   <xsl:apply-templates/>
   </table>
   <h3>Summary</h3>
	<ul>
	<li><a href="#choice">Choice Recommendation</a></li>
	<li><a href="#graph">Outranking digraph</a></li>
	<li><a href="#actions">Potential decision actions</a></li>
	<li><a href="#performance">Performance table</a></li>
	<li><a href="#criteria">Family of criteria</a></li>
	<li><a href="#outranking">Outranking relation</a></li>	
	<li><a href="#vetos">Veto situations</a></li>	
	</ul>
</xsl:template>

<xsl:template match="name">
   <tr><th align="left">Name: </th><th align="left"><font color="#0000bb"><xsl:apply-templates/></font></th></tr>
   <tr><th align="left">Category: </th><td><xsl:value-of select="/rubisOutrankingDigraph/@category"/></td></tr>
   <tr><th align="left">Subcategory: </th><td><xsl:value-of select="/rubisOutrankingDigraph/@subcategory"/></td></tr>
</xsl:template>

<xsl:template match="author">
   <tr><th align="left">Author: </th><td><xsl:apply-templates/></td></tr>
</xsl:template>

<xsl:template match="reference">
   <tr><th align="left">Reference: </th><td><em><xsl:apply-templates/></em></td></tr>
</xsl:template>

<xsl:template match="actions">
   <h2><a name="actions"><font color="#bb0000">Actions</font></a></h2>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Identifyer</th>
        <th>Name</th>
        <th>Comment</th>
      </tr>
   <xsl:for-each select="action">
       <tr><td><xsl:number format="1"/></td>
           <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
           <td><xsl:value-of select="name"/></td>
           <td><xsl:value-of select="comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="criteria">
   <h2><a name="criteria"><font color="#bb0000">Criteria</font></a></h2>
   <table border="1">
     <tr bgcolor="#9acd32">
        <th rowspan="2">#</th>
        <th rowspan="2">Identifyer</th>
        <th rowspan="2">Name</th>
        <th rowspan="2">Comment</th>
        <th rowspan="2">Weight</th>
	<th rowspan="2">Scale</th>
	<th colspan="5">Thresholds</th>
     </tr>
     <tr bgcolor="#9acd32">
	<th>indifference</th>
	<th>weak preference</th>
	<th>preference</th>
	<th>weak veto</th>
	<th>veto</th>
      </tr>
   <xsl:for-each select="criterion">
       <tr>
         <td><xsl:number format="1"/></td>
        <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
	   <td><xsl:value-of select="name"/></td>
	   <td><xsl:value-of select="comment"/></td>
	   <td><xsl:value-of select="weight"/></td>
	   <td>(<xsl:value-of select="scale/min"/>,<xsl:value-of select="scale/max"/>)</td>
	   <td align="center"><xsl:value-of select='thresholds/indifference'/></td>
	   <td align="center"><xsl:value-of select='thresholds/weakPreference'/></td>
	   <td align="center"><xsl:value-of select='thresholds/preference'/></td>
	   <td align="center"><xsl:value-of select='thresholds/weakVeto'/></td>
	   <td align="center"><xsl:value-of select='thresholds/veto'/></td></tr>          
   </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="evaluations">
   <h2><a name="performance"><font color="#bb0000">Performance Table</font></a></h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>criterion</th>
	<xsl:for-each select="/rubisOutrankingDigraph/actions/action">
	  <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      <xsl:apply-templates/>
    </table>
</xsl:template>

<xsl:template match="evaluation">
  <tr>
    <th bgcolor="#FFF79B"><xsl:value-of select="criterionID"/></th>
    <xsl:for-each select="performance">
      <td align="right"><xsl:value-of select='value'/></td>
    </xsl:for-each> 
  </tr>
</xsl:template>

<xsl:template match="valuationDomain">   
     <h3><font color="#0000bb">Valuation domain of the outranking credibility</font></h3>
    <table border="1">
      <tr><td bgcolor="#FFF79B">Maximum - certainly validated</td> <td align="right" bgcolor="#ddffdd"> <xsl:value-of select="max"/></td></tr>
      <tr><td bgcolor="#FFF79B">Median - indeterminate</td> <td align="right" bgcolor="#dddddd" ><xsl:value-of select="med"/></td></tr>
      <tr><td bgcolor="#FFF79B">Minimum - certainly not validated</td> <td align="right" bgcolor="#ffddff" ><xsl:value-of select="min"/></td></tr>
    </table>
</xsl:template>

<xsl:template match="min">
	Minimum: <xsl:apply-templates/><br/>
</xsl:template>

<xsl:template match="max">
	Maximum: <xsl:apply-templates/>
</xsl:template>


<xsl:key name="relationRow" match="relation/arc/initialActionID" use='.'  ></xsl:key>

<xsl:variable name="allRows" 
  select="/rubisOutrankingDigraph/relation/arc/initialActionID[ 
  generate-id() = 
  generate-id(key('relationRow',.)[1] 
  )
  ]" />
  
<xsl:template match="relation">
     <xsl:variable name="Med" select="/rubisOutrankingDigraph/valuationDomain/min + (/rubisOutrankingDigraph/valuationDomain/max - /rubisOutrankingDigraph/valuationDomain/min) div 2"/>
     <h2><a name="outranking"><font color="#bb0000">Bipolar-valued Outranking Relation</font></a></h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>(x S y)</th>
        <xsl:for-each select="/rubisOutrankingDigraph/actions/action">
	  <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      <xsl:for-each select="$allRows">
        <tr>
            <xsl:variable name="currentRow" select='.' />
            <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow" /></th>
            <xsl:for-each select="key('relationRow', $currentRow)">
                <xsl:variable name="arcValue" select="./parent::arc"/>
                <xsl:choose>
                  <xsl:when test="$arcValue/value &gt; /rubisOutrankingDigraph/valuationDomain/max">
                    <td>Error: value too high</td>
                  </xsl:when>
                  <xsl:when test="$arcValue/value &lt; /rubisOutrankingrubisOutrankingDigraph/valuationDomain/min">
                    <td>Error: value too low</td>
                  </xsl:when>
                  <xsl:when test="$arcValue/value &gt; $Med">
                    <td bgcolor="#ddffdd" align="right" >
                      <xsl:value-of select="$arcValue/value"/></td>
                  </xsl:when>
                  <xsl:when test="$arcValue/value &lt; $Med">
                    <td bgcolor="#ffddff"  align="right">
                      <xsl:value-of select="$arcValue/value"/></td>
                  </xsl:when>
                  <xsl:otherwise>
                    <td bgcolor="#dddddd" align="right" >
                      <xsl:value-of select="$arcValue/value"/></td>
                  </xsl:otherwise>
                </xsl:choose>
             </xsl:for-each>
         </tr>
       </xsl:for-each>
  </table>

  <h2><a name="graph"><font color="#bb0000">Significantly concordant outranking digraph</font></a></h2>
  <p>(<i><b> Black arrows</b> indicate outranking situations supported by a criteria coalition 
    of positive significance, i.e. gathering more than 50&#37; of the global criteria significance weights.
    <b>Empty arrow heads</b> indicate an indeterminate outranking situation.</i>)</p>
  <xsl:variable name="tiret" select=" '-' " />
  <xsl:variable name="dot" select=" '.' " />
  <xsl:variable name="name" select ="/rubisOutrankingDigraph/header/name" />
  <xsl:variable name="path" select=" 'http://ernst-schroeder.uni.lu/rubisServer/Images/rubisGraph-' " />
  <xsl:variable name="extension" select=" '.png' " />	
  <div style="text-align: left;">	
    <img src="{concat($path,substring-before(substring-after($name,$tiret),$dot),$extension)}"  />
  </div> 
  
</xsl:template>

<xsl:template match="vetos">
  <h3><a name="vetos"><font color="#bb0000">Veto situations</font></a></h3>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="veto/arc">
  <h4>Arc: (<xsl:value-of select="initialActionID"/>,<xsl:value-of select="terminalActionID"/>), concordance degree: <xsl:value-of select="concordanceDegree"/></h4>
</xsl:template>

<xsl:template match="vetoSituations">
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>criterion</th>
        <th>performance difference</th>
	<th>veto characteristic</th>
	<th>comment</th>
      </tr>

      <xsl:for-each select="vetoSituation">
	<tr>
        <th bgcolor="#FFF79B"><xsl:value-of select="criterionID"/></th>
        <td align="right"><xsl:value-of select="performanceDifference"/></td>
        <td align="right"><xsl:value-of select="vetoCharacteristic"/></td>
        <td><xsl:value-of select="comment"/></td>
	</tr>
      </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="choiceRecommendation">
   <h2><a name="choice"><font color="#0000bb">Rubis choice recommendation</font></a></h2>
   <xsl:apply-templates/>
</xsl:template>
<xsl:template match="cocaActions">
   <table border="1">
     <tr bgcolor="#9acd32"><th colspan="4" >Coca digraph actions</th></tr>
     <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Identifyer</th>
        <th>Name</th>
        <th>Comment</th>
      </tr>
   <xsl:for-each select="cocaAction">
       <tr><td><xsl:number format="1"/></td>
           <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
           <td><xsl:value-of select="name"/></td>
           <td><xsl:value-of select="comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="goodChoices">
   <h3><font color="#bb0000">Good choice recommendations</font></h3>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>Choice set</th>
      <th>Determinateness</th>
      <th>Outrankingness</th>
      <th>Outrankedness</th>
      <th>Independence</th>
    </tr>
   <xsl:for-each select="choiceSet">
     <tr>
       <th bgcolor="#FFF79B"><xsl:apply-templates/></th>
       <td align="right"><xsl:value-of select="@determinateness"/></td>
       <td align="right"><xsl:value-of select="@outranking"/></td>
       <td align="right"><xsl:value-of select="@outranked"/></td>
       <td align="right"><xsl:value-of select="@independence"/></td>
     </tr>
      </xsl:for-each>
     </table>
</xsl:template>
  
<xsl:template match="badChoices">
   <h3><font color="#bb0000">Potentially bad choices</font></h3>
    <table border="1">
    <tr bgcolor="#9acd32">
      <th>Choice set</th>
      <th>Determinateness</th>
      <th>Outrankedness</th>
      <th>Outrankingness</th>
      <th>Independence</th>
    </tr>
    <xsl:for-each select="choiceSet">
     <tr>
       <th bgcolor="#ADD8E6"><xsl:apply-templates/></th>
       <td align="right"><xsl:value-of select="@determinateness"/></td>
       <td align="right"><xsl:value-of select="@outranked"/></td>
       <td align="right"><xsl:value-of select="@outranking"/></td>
       <td align="right"><xsl:value-of select="@independence"/></td>
     </tr>
      </xsl:for-each>
      </table>
</xsl:template>

  <xsl:template match="choiceActions">
    <xsl:text>{</xsl:text> 
    <xsl:for-each select="actionID"><xsl:value-of select="descendant-or-self::text()"/><xsl:text>,</xsl:text>            
    </xsl:for-each><xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="comment">
  <!-- no comments -->
</xsl:template>

</xsl:stylesheet>
