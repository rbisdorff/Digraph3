<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">
  
<!-- 
XMCDA 2.0 Rubis XSLT tranformation to HTML, RB 2017
$Revision: 1.0 $
The ressource comes with ABSOLUTELY NO WARRANTY 
to the extent permitted by the applicable law.
This is free software, and you are welcome to 
redistribute it if it remains free software. 
Copyright (C) 2009 DECISION DECK Consortium
Copyright (C) 2009-2017 Raymond Bisdorff Luxembourg
-->


 <!-- Main start of the transform -->
  
<xsl:template match="/" >
 <html>
  <head><title>D2-Decision-Deck UMCDA-ML XMCDA-2.0 application</title></head>
  <body>
    <h2><font color="#0000bb">Decision-Deck UMCDA-ML XMCDA 2.0 application</font></h2>
    
    <xsl:apply-templates />
    <hr />
    <p><b>Rubis XSLT to HTML stylesheet (R. Bisdorff):</b> $Revision: 1.7 $ <br/>
          UMCDA-ML <a href="http://www.decision-deck.org/xmcda">XMCDA 2.0 Schema</a><br/>
          Raymond Bisdorff (University of Luxembourg), Patrick Meyer (Telecom Bretagne) and Thomas Veneziano (University of Luxembourg)March 2009<br/>
          Copyright © 2009 <a href="http://www.decision-deck.org/">DECISION DECK Consortium</a><br/>
          <a href="javascript:void(document.location='view-source:'+document.location)">View the source of this document.</a></p>
   </body>
  </html>
</xsl:template>
 
  <xsl:template match="alternativesComparisions[@mcdaConcept='outrankingDigraph']" mode="toc">
     <!-- <xsl:apply-templates select="."/> -->
    <li><a href="#digraph">Outranking Digraph</a></li>
  </xsl:template>
 
  <xsl:template match="alternativesComparisions[@mcdaConcept='ValuedDigraph']" mode="toc">
     <!-- <xsl:apply-templates select="."/> -->
    <li><a href="#digraph">Valued Digraph</a></li>
  </xsl:template>
 
 <!--  generic description layout: must fit all element description !!! -->
  
  <xsl:template match="description" mode="bipolar">
     <xsl:apply-templates select="."/>
  </xsl:template>
 
  <xsl:template match="description" mode="veto">
     <xsl:apply-templates select="."/>
  </xsl:template>
  
  <xsl:template match="description" mode="simil">
     <xsl:apply-templates select="."/>
  </xsl:template>
  
  <xsl:template match="title">
    <h1><font color="#bb0000"><xsl:value-of select="text()"/></font></h1>
  </xsl:template>
  
  <xsl:template match="subTitle">
    <h2><font color="#0000bb"><xsl:value-of select="text()"/></font></h2>
  </xsl:template>
  
  <xsl:template match="subSubTitle">
    <h3><font color="#0000bb"><xsl:value-of select="text()"/></font></h3>
  </xsl:template>
  
  <xsl:template match="id">
    Identifier: <font color="#0000bb"><xsl:value-of select="text()" /></font><br/>
  </xsl:template>
  
  <xsl:template match="approach">
    Approach: <font color="#0000bb"><xsl:value-of select="text()" /></font><br/>
  </xsl:template>
  
  <xsl:template match="methodology">
    Methodology: <font color="#0000bb"><xsl:value-of select="text()" /></font><br/>
  </xsl:template>
  
  <xsl:template match="problematique">
    Problematique: <font color="#0000bb"><xsl:value-of select="text()" /></font><br/>
  </xsl:template>
  
  <xsl:template match="shortName">
    Short name: <xsl:value-of select="text()" /><br/>
  </xsl:template>
  
  <xsl:template match="name">
    Name: <font color="#0000bb"><xsl:value-of select="text()" /></font><br/>
  </xsl:template>
  
  <xsl:template match="comment">
    Comment: <em><xsl:value-of select="text()" /></em>
  </xsl:template>
  
  <xsl:template match="author">
    Author: <xsl:apply-templates/><br/>
  </xsl:template>
  
  <xsl:template match="user">
    User: <xsl:apply-templates/><br/>
  </xsl:template>
  
  <xsl:template match="type">
 <!--    <tr><th align="left">Type: </th><td><xsl:apply-templates/></td></tr> -->
  </xsl:template>
  
  <xsl:template match="version">
    Version: <xsl:apply-templates/><br/>
  </xsl:template>
  
  <xsl:template match="abstract">
    Abstract: <em><xsl:value-of select="text()" /></em><br/>
  </xsl:template>
  
  <xsl:template match="keywords">
    Key Words: <xsl:value-of select="text()" /><br/>
  </xsl:template>
  
  <xsl:template match="bibliography">
    <xsl:apply-templates  select="description"/>
    <table border="0">
    <xsl:for-each select="bibEntry">
      <tr>
        <td><xsl:number format="1"/></td>
        <td><xsl:value-of select="text()"/></td>
      </tr>
    </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="dateTime">
    Date: <xsl:value-of select="text()" /><br/>
  </xsl:template>
  
<!-- Method Data -->
<xsl:template match="methodParameters">
   <xsl:apply-templates/>
</xsl:template>

  <xsl:template match="parameters">
    <table cellpadding="1" border="1">
      <tr><th bgcolor="#9acd32">Parameter</th><th bgcolor="#9acd32">Value</th><th bgcolor="#9acd32">Comment</th></tr>
      <xsl:apply-templates/>
    </table>
  </xsl:template>
  
  <xsl:template match="parameter[value]">
    <tr><td bgcolor="#FFF79B"><xsl:value-of select="@name"/></td><td><xsl:value-of select="value"/></td><td><xsl:value-of select="description/comment"/></td></tr>
  </xsl:template>
  <xsl:template match="parameter[function/constant]">
    <tr><td bgcolor="#FFF79B"><xsl:value-of select="@name"/></td><td><xsl:value-of select="function"/></td><td><xsl:value-of select="description/comment"/></td></tr>
  </xsl:template>
  <xsl:template match="parameter[function/linear]">
    <tr><td bgcolor="#FFF79B"><xsl:value-of select="@name"/></td><td><xsl:value-of select="function/linear/intercept"/>+<xsl:value-of select="function/linear/slope"/>x</td><td><xsl:value-of select="description/comment"/></td></tr>
  </xsl:template>
  
  
  <xsl:template match="errorMessage">
 <table cellpadding="1" border="1">
   <tr><th bgcolor="#9acd32">Number</th><th bgcolor="#9acd32">Name</th><th bgcolor="#9acd32">Text</th></tr>
   <tr><td bgcolor="#FFF79B"><xsl:value-of select="number"/></td><td><xsl:value-of select="@name"/></td><td><xsl:value-of select="text"/></td></tr>
   </table>
</xsl:template>


<xsl:template match="alternatives">
  <a name="alternatives"/>
   <xsl:apply-templates  select="description"/>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Identifyer</th>
        <th>Name</th>
        <th>Comment</th>
      </tr>
   <xsl:for-each select="alternative">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
           <td><xsl:value-of select="@name"/></td>
           <td><xsl:value-of select="description/comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>
  
 
  <xsl:template match="alternativesComparisons">
    <a name="digraph"/>
    <xsl:choose>
      <xsl:when test="valuation/valuationType='bipolar'">
        <xsl:apply-templates mode="bipolar"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
 
  <xsl:template match="relationOnCriteria">
    <a name="correlation"/>
     <xsl:apply-templates mode="simil"/>
  </xsl:template>
 
  <xsl:template match="relationOnAlternatives[description/type='Vetoes']" >
        <xsl:apply-templates mode="veto"/>
  </xsl:template>
  
  <xsl:template match="valuation" mode="bipolar">
       <xsl:apply-templates select="description"/>
       <xsl:variable name="median" select="quantitative/minimum + (quantitative/maximum - quantitative/minimum) div 2"></xsl:variable>
       <table cellpadding="1" border="1">
         <tr><td bgcolor="#FFF79B">Maximum</td><td bgcolor="#ddffdd" align="right"><xsl:value-of select="quantitative/maximum"/></td></tr>
         <tr><td bgcolor="#FFF79B">Median</td><td bgcolor="#dddddd"  align="right"><xsl:value-of select="$median" /></td></tr>
         <tr><td bgcolor="#FFF79B">Minimum</td><td bgcolor="#ffddff"  align="right"><xsl:value-of select="quantitative/minimum"/></td></tr>
       </table>
    
  </xsl:template>
   
  <xsl:template match="valuation">
       <xsl:apply-templates select="description"/>
        <table cellpadding="1" border="1">
         <tr><td bgcolor="#FFF79B">Minimum</td><td align="right"><xsl:value-of select="quantitative/minimum"/></td></tr>
         <tr><td bgcolor="#FFF79B">Maximum</td><td align="right"><xsl:value-of select="quantitative/maximum"/></td></tr>
        </table>
  </xsl:template>
  
  <xsl:template match="comparisonType">
    
  </xsl:template>
 
  <xsl:template match="comparisonType" mode="bipolar">
    
  </xsl:template>
 
  <xsl:template match="pairs" mode="veto">
       <xsl:variable name="Veto" select='.' />
       <xsl:apply-templates select="description"/>
       <ol>
        <xsl:for-each select="$Veto/pair">
           <li>Veto against <b><xsl:value-of select="initial/alternativeID"/> outranks
            <xsl:value-of select="terminal/alternativeID"/> </b> (
          <xsl:value-of select="description/comment"/>)
           <table border="1">
             <tr bgcolor="#9acd32"><th>criterion</th><th>performance difference</th><th>status</th><th>characteristic</th></tr>
             <xsl:for-each select="values">
               <tr>
                 <th bgcolor="#FFF79B" align="center"><xsl:value-of select="@id"/></th>
                 <td align="center"><xsl:value-of select="value[@name='performanceDifference']/real"/></td>
                 <td><xsl:value-of select="description/comment"/></td>
                 <td align="center"><xsl:value-of select="value[@name='vetoCharacteristic']/real"/></td>
               </tr>
             </xsl:for-each>
             </table><br/>
           </li>
        </xsl:for-each>
         </ol>
  </xsl:template>
   
  <xsl:template match="pairs">
    <xsl:variable name="currentArcs" select="."/>
    <xsl:variable name="allAlternatives" select="/xmcda:XMCDA/alternatives/alternative"/>
    <xsl:apply-templates select="description"/>
    -->
    <table border="1">
      <tr bgcolor="#9acd32">
        <th><xsl:value-of select="preceding::comparisonType"/></th>
        <xsl:for-each select="$allAlternatives">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
      <xsl:for-each select="$allAlternatives">
                   <xsl:variable name="currentRow" select='@id' />
       <tr>
        <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
         <xsl:for-each select="$allAlternatives">
          <xsl:variable name="currentColumn" select='@id' />
          <xsl:for-each select="$currentArcs/pair[initial/alternativeID=$currentRow]">
            <xsl:variable name="currentArc" select="."></xsl:variable>
            <xsl:call-template name="currentValue" >
              <xsl:with-param name="currentRow" select="$currentRow" />   
              <xsl:with-param name="currentColumn" select="$currentColumn"/>                  
              <xsl:with-param name="currentArc" select="$currentArc" />
             </xsl:call-template>
           </xsl:for-each>
        </xsl:for-each>
      </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="pairs" mode="bipolar">
    <xsl:variable name="currentArcs" select="."/>
    <xsl:variable name="allAlternatives" select="/xmcda:XMCDA/alternatives/alternative"/>
    <xsl:apply-templates select="description"/>
    
    <table border="1">
      <tr bgcolor="#9acd32">
        <th><xsl:value-of select="preceding::comparisonType"/></th>
        <xsl:for-each select="$allAlternatives">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
      <xsl:variable name="Min" select="parent::node()/valuation/quantitative/minimum"/>
      <xsl:variable name="Max" select="parent::node()/valuation/quantitative/maximum"/>
      <xsl:variable name="Med" select="$Min + ($Max - $Min) div 2"/>
      
      <xsl:for-each select="$allAlternatives">
        <xsl:variable name="currentRow" select='@id' />
        <tr>
          <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
          <xsl:for-each select="$allAlternatives">
            <xsl:variable name="currentColumn" select='@id' />
            <xsl:for-each select="$currentArcs/pair[initial/alternativeID=$currentRow]">
              <xsl:variable name="currentArc" select="."></xsl:variable>
              <xsl:call-template name="currentBipolarValue" >
                <xsl:with-param name="currentRow" select="$currentRow" />   
                <xsl:with-param name="currentColumn" select="$currentColumn"/>                  
                <xsl:with-param name="currentArc" select="$currentArc" />
                <xsl:with-param name="Med" select="$Med" />
              </xsl:call-template>
            </xsl:for-each>
          </xsl:for-each>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="pairs" mode="simil">
    <xsl:variable name="currentArcs" select="."/>
    <xsl:apply-templates select="description"/>

    <table border="1">
      <tr bgcolor="#9acd32">
        <th>relation</th>
        <xsl:for-each select="/xmcda:XMCDA/criteria/criterion">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
      <xsl:for-each select="/xmcda:XMCDA/criteria/criterion">
                   <xsl:variable name="currentRow" select='@id' />
       <tr>
        <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
         <xsl:for-each select="/xmcda:XMCDA/criteria/criterion">
          <xsl:variable name="currentColumn" select='@id' />
          <xsl:for-each select="$currentArcs/arc[from/criterionID=$currentRow]">
            <xsl:variable name="currentArc" select="."></xsl:variable>
            <xsl:call-template name="currentSimilValue" >
              <xsl:with-param name="currentRow" select="$currentRow" />   
              <xsl:with-param name="currentColumn" select="$currentColumn"/>                  
              <xsl:with-param name="currentArc" select="$currentArc" />
             </xsl:call-template>
           </xsl:for-each>
        </xsl:for-each>
      </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  

 
  <xsl:template name="currentSimilValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
    <xsl:if test="$currentArc[initial/criterionID=$currentRow]">
      <xsl:if test="$currentArc[terminal/criterionID=$currentColumn]">
        <xsl:variable name="arcValue" select="$currentArc/value"></xsl:variable>
        <xsl:choose>
          <xsl:when test="$arcValue &gt; 0.0">
            <td bgcolor="#ddffdd" align="right" >
              <xsl:value-of select="$arcValue"/></td>
          </xsl:when>
          <xsl:when test="$arcValue &lt; 0.0">
            <td bgcolor="#ffddff"  align="right">
              <xsl:value-of select="$arcValue"/></td>
          </xsl:when>
          <xsl:otherwise>
            <td bgcolor="#dddddd" align="right" >
              <xsl:value-of select="$arcValue"/></td>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="currentValue" match="pair" >
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
    <xsl:if test="$currentArc[initial/alternativeID=$currentRow]">
      <xsl:if test="$currentArc[terminal/alternativeID=$currentColumn]">
        <td align="right" ><xsl:value-of select="./value"/></td>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="currentBipolarValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
      <xsl:param name="Med"/>
    <xsl:if test="$currentArc[initial/alternativeID=$currentRow]">
      <xsl:if test="$currentArc[terminal/alternativeID=$currentColumn]">
        <xsl:variable name="arcValue" select="$currentArc/value"></xsl:variable>
        <xsl:choose>
          <xsl:when test="$arcValue &gt; $Med">
            <td bgcolor="#ddffdd" align="right" >
              <xsl:value-of select="$arcValue"/></td>
          </xsl:when>
          <xsl:when test="$arcValue &lt; $Med">
            <td bgcolor="#ffddff"  align="right">
              <xsl:value-of select="$arcValue"/></td>
          </xsl:when>
          <xsl:otherwise>
            <td bgcolor="#dddddd" align="right" >
              <xsl:value-of select="$arcValue"/></td>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:if>
  </xsl:template>


<!-- presentation of the objectives-->
  
<xsl:template match="objectives">
  <a name="objectives"/>
  <xsl:apply-templates  select="description"/>
   <table border="1">
     <tr bgcolor="#9acd32">
        <th rowspan="1">#</th>
        <th rowspan="1">Identifyer</th>
        <th rowspan="1">Name</th>
        <th rowspan="1">Comment</th>
        <th rowspan="1">Criteria list</th>
     </tr>
     <xsl:for-each select="objective">
       <tr>
         <td align="center"><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
	   <td><xsl:value-of select="@name"/></td>
	   <td><xsl:value-of select="description/comment"/></td>        
         <td align="center"><xsl:value-of select="objectiveCriteria"/></td>
       </tr>
     </xsl:for-each>
   </table>
</xsl:template>

<!-- presentation of the coalitions -->
<xsl:template match="criteriaSets">
  <a name="coalitions"/>
  <xsl:apply-templates  select="description"/>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th rowspan="1">#</th>
      <th rowspan="1">Identifyer</th>
      <th rowspan="1">Name</th>
      <th rowspan="1">Criteria</th>
      <th rowspan="1">Comment</th>
    </tr>
   <xsl:for-each select="criteriaSet">
      <tr>
        <td align="center"><xsl:number format="1"/></td>
        <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        <td><xsl:value-of select="@name"/></td>
       <td>{
          <xsl:for-each select="element"><xsl:value-of select="criterionID"/>, </xsl:for-each>
          }</td>
        <td><xsl:value-of select="description/comment"/></td>
        </tr>
    </xsl:for-each>
  </table>
</xsl:template>
  
<!-- presentation of the criteria -->
  
<xsl:template match="criteria">
  <a name="criteria"/>
  <xsl:apply-templates  select="description"/>
   <table border="1">
     <tr bgcolor="#9acd32">
        <th rowspan="2">#</th>
        <th rowspan="2">Identifyer</th>
        <th rowspan="2">Name</th>
        <th rowspan="2">Comment</th>
        <th rowspan="2">Weight</th>
	<th colspan="3">Scale</th>
	<th colspan="5">Thresholds</th>
     </tr>
     <tr bgcolor="#9acd32">
       <th>direction</th>
       <th>min</th>
       <th>max</th>
       <th>indifference</th>
       <th>weak preference</th>
       <th>preference</th>
       <th>weak veto</th>
       <th>veto</th>
      </tr>
     <xsl:for-each select="criterion">
       <tr>
         <td align="center"><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
	   <td><xsl:value-of select="@name"/></td>
	   <td><xsl:value-of select="description/comment"/></td>        
         <td align="center"><xsl:value-of select="criterionValue/."/></td>
	   <td align="center"><xsl:value-of select="scale/quantitative/preferenceDirection"/></td>
         <td align="center"><xsl:value-of select="scale/quantitative/minimum/."/></td>
         <td align="center"><xsl:value-of select="scale/quantitative/maximum/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='ind']"/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakPreference']"/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='pref']"/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakVeto']"/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='veto']"/></td></tr>
     </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="constant">
  <!--<xsl:if test="descendant::*name()= 'linear'">integer<xsl:value-of select="."/></xsl:if>
  <xsl:value-of select="."/> -->
  <xsl:apply-templates/>
</xsl:template>

<!--<xsl:template match="value/integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>
-->
  <xsl:template match="integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>
<!--<xsl:template match="value/real">
  <xsl:value-of select="format-number(.,'#.##')"/>
</xsl:template>
-->
  <xsl:template match="real">
  <xsl:value-of select="format-number(.,'#.##')"/>
</xsl:template>

  <!--<xsl:template match="value/rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>
-->
<xsl:template match="rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>

<xsl:template match="linear">
  <xsl:value-of select="intercept/."/> + <xsl:value-of select="slope/."/>x
</xsl:template>



  <!-- Controlling the presentation of the performance table -->
  <xsl:key name="currentCriterion" match="/xmcda:XMCDA/criteria/criterion" use='.'  />
  
  <xsl:variable name="allCriteria" 
    select="/xmcda:XMCDA/criteria/criterion[
    generate-id() = 
    generate-id(key('currentCriterion',.)[1] 
    )
    ]" />  
  
  
<xsl:template match="performanceTable">
  <xsl:variable name="root" select="/xmcda:XMCDA/criteria"></xsl:variable>
   <xsl:variable name="currentTable" select="."></xsl:variable>
    <xsl:apply-templates  select="description"/>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>alternative</th>
        <xsl:for-each select="$root/criterion">
	  <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      <xsl:apply-templates select="$currentTable/alternativePerformances"/> 
    </table>
</xsl:template>

<xsl:template match="alternativePerformances">
  <tr>
    <th bgcolor="#FFF79B"><xsl:value-of select="alternativeID"/></th>
    <xsl:variable name="currentAlternative" select="."></xsl:variable>

   <xsl:for-each select="key('currentCriterion', $allCriteria)">
      <xsl:variable name="currentCriterion" select="./@id"></xsl:variable>
       <xsl:call-template name="performanceRow">
         <xsl:with-param name="currentAlternative" select="$currentAlternative" />
         <xsl:with-param name="currentCriterion" select="$currentCriterion"/>
       </xsl:call-template>
      </xsl:for-each>
  </tr>
</xsl:template>

<xsl:template name="performanceRow">
      <xsl:param name="currentAlternative"></xsl:param>
      <xsl:param name="currentCriterion"></xsl:param>
      <xsl:variable name="currentPerformance" select="$currentAlternative/performance[criterionID=$currentCriterion]"></xsl:variable>
     <td align="right"><xsl:apply-templates select="$currentPerformance/value"/></td>
</xsl:template>

<!-- <xsl:template match="comment"> -->
  <!-- no comments -->
<!-- </xsl:template> -->
<xsl:template match="XMCDA/alternatives/description">
  <!-- no comments -->
</xsl:template>

<xsl:template match="choices">
    <a name="choices"></a>
   <xsl:apply-templates  select="description"/>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Choice set</th>
        <th>Determinateness</th>
        <th>Outrankingness</th>
        <th>Outrankedness</th>
        <th>Comment</th>
      </tr>
   <xsl:for-each select="choice">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B">{
           <xsl:for-each select="choiceMembersList/choiceMember">
             <xsl:value-of select="./alternativeID"/>,
           </xsl:for-each>}
           </th>
           <td align="center"><xsl:value-of select="qualities/parameter[name='determinateness']/value"/></td>
           <td align="center"><xsl:value-of select="qualities/parameter[name='outranking']/value"/></td>
         <td align="center"><xsl:value-of select="qualities/parameter[name='outranked']/value"/></td>
         <td><xsl:value-of select="description/comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>
 
</xsl:stylesheet>
    