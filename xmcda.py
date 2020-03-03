#!/Usr/bin/env python3
"""
Python3+ implementation of xmcda tools
Copyright (C) 2016-2020  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################
__version__ = "Branch: 3.5 $"
# ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3

"""
XMCDA 2.0 xsl style sheets and XMCDA save and show method
for the Rubis best-choice recommendation.
"""
import sys,copy,string,os,tempfile
import codecs
from outrankingDigraphs import *
from xmcda import *

############################
rubisExtXSL =\
"""<?xml version="1.0" encoding="utf-8"?>
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
    <p><b>Rubis XSLT to HTML stylesheet (R. Bisdorff):</b> $Revision: 1.0$ <br/>
          UMCDA-ML <a href="http://www.decision-deck.org/xmcda">XMCDA 2.0 Extended Schema</a><br/>
          Raymond Bisdorff (University of Luxembourg), Patrick Meyer (Telecom Bretagne) and Thomas Veneziano (University of Luxembourg)March 2009<br/>
          Copyright © 2009-2017 <a href="http://www.decision-deck.org/">DECISION DECK Consortium</a><br/>
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
    """

rubisXSL =\
"""<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">
  
<!-- 
XMCDA 2.0 Default XSLT tranformation to HTML, RB 2009
$Revision: 1.7 $
The ressource comes with ABSOLUTELY NO WARRANTY 
to the extent permitted by the applicable law.
This is free software, and you are welcome to 
redistribute it if it remains free software. 
Copyright (C) 2009 DECISION DECK Consortium
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
    """
####################
rubisChoiceXSL =\
"""<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                       xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">
  
<!-- 
XMCDA 2.0 Rubis XSLT tranformation to HTML, RB 2009
$Revision: 1.6 $
The ressource comes with ABSOLUTELY NO WARRANTY 
to the extent permitted by the applicable law.
This is free software, and you are welcome to 
redistribute it if it remains free software. 
Copyright (C) 2009 DECISION DECK Consortium
-->


 <!-- Main start of the transform -->
  
<xsl:template match="/" >
 <html>
  <head><title>Decision-Deck UMCDA-ML-2.0 application</title></head>
  <body>
    <h1><font color="#0000bb">Decision-Deck UMCDA-ML-2.0 Application</font></h1>

    <xsl:apply-templates  select="xmcda:XMCDA" />
    <br/>
    <h2>Content</h2>
    <ul>
      <li><a href="#choice">Choice Recommendation</a></li>
      <li><a href="#graph">Outranking digraph</a></li>
      <li><a href="#alternatives">Potential decision actions</a></li>
      <li><a href="#performance">Performance table</a></li>
      <li><a href="#criteria">Family of criteria</a></li>
      <li><a href="#correlation">Criteria ordinal correlation</a></li>
      <li><a href="#outranking">Outranking relation</a></li>	
      <li><a href="#vetos">Veto situations</a></li>	
      <li><a href="#notice">Notice</a></li>	
    </ul>
    <hr />
    <h2><a name="notice"><font color="#bb0000">Notice</font></a></h2>
    <p>Bisdorff R., Meyer P., Roubens M., <b>Rubis</b>: A new methodology for the choice decision problem. 4OR, 
      <em>A Quarterly Journal of Operational Research</em>, Springer (2008), Vol 6 Number 2 pp. 143-165, DOI 10.1007/s10288-007-0045-5.
    <a href="http://sma.uni.lu/bisdorff/documents/HyperKernels.pdf">PDF preprint version</a>.</p>
   <p>Online documentation: <a href="https://www.decision-deck.org">Decision Deck Project</a><br/>
     <b>Rubis XSL Transformation to HTML</b> R. Bisdorff, $Revision: 1.6 $<br/>
          <a href="http://www.decision-deck.org/xmcda">XMCDA 2.0 Schema</a> P. Meyer and Th. Veneziano 2009 <br/>
           Copyright © 2009 DECISION DECK Consortium</p>
   </body>
  </html>
</xsl:template>
 

 <!--  generic description layout: must fit all element description !!! -->
  
  <xsl:template match="projectReference">
     <xsl:apply-templates />
    <h3>Content</h3>
    <ul>
      <li><a href="#choice">Choice Recommendation</a></li>
      <li><a href="#graph">Outranking digraph</a></li>
      <li><a href="#alternatives">Potential decision actions</a></li>
      <li><a href="#performance">Performance table</a></li>
      <li><a href="#criteria">Family of criteria</a></li>
      <li><a href="#correlation">Criteria ordinal correlation</a></li>
      <li><a href="#outranking">Outranking relation</a></li>	
      <li><a href="#vetos">Veto situations</a></li>	
      <li><a href="#notice">Notice</a></li>	
    </ul>
  </xsl:template>
  
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
    <h2><font color="#bb0000"><xsl:value-of select="text()"/></font></h2>
  </xsl:template>
  
  <xsl:template match="subTitle">
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
    Comment: <em><xsl:value-of select="text()" /></em><br/>
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

<!--  Method Options  -->

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

<!-- List of potential alternatives -->
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

  <!-- relation on Alternatives -->
  <xsl:template match="alternativesComparisons[@mcdaConcept='outrankingDigraph']">
    <h2><a name="graph"><font color="#bb0000">Significantly Concordant Outranking Graph</font></a></h2>
    <p>(<i><b> Black arrows</b> indicate outranking situations supported by a criteria coalition 
      of positive significance, i.e. gathering more than 50&#37; of the global criteria significance weights.
      <b>Empty arrow heads</b> indicate an indeterminate outranking situation.</i>)</p>
    <xsl:variable name="tiret" select=" '-' " />
    <xsl:variable name="dot" select=" '.' " />
    <xsl:variable name="name" select ="/xmcda:XMCDA/@instanceID" />
    <xsl:variable name="path" select=" 'rubisGraph-' " />
    <xsl:variable name="extensionPNG" select=" '.png' " />
    <xsl:variable name="extensionPDF" select=" '.pdf' " />
    <div style="text-align: left;">	
      <p><a href="{concat($path,$name,$extensionPDF)}" >
      See PDF graphic file for better image quality and zooming options</a>
        (generated with GraphViz).</p> 
      <img src="{concat($path,$name,$extensionPNG)}"  />   
    </div> 
    
    <a name="outranking"/>
    <xsl:choose>
      <xsl:when test="valuation/valuationType='bipolar'">
        <xsl:apply-templates mode="bipolar"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
 
  <xsl:template match="criteriaComparisons[@mcdaConcept='correlationTable']">
    <a name="correlation"/>
    <xsl:apply-templates mode="simil"/>
    <xsl:variable name="tiret" select=" '-' " />
    <xsl:variable name="dot" select=" '.' " />
    <xsl:variable name="name" select ="/xmcda:XMCDA/@instanceID" />
    <xsl:variable name="path" select=" 'similarityPlot-' " />
    <xsl:variable name="extensionPDF" select=" '.pdf' " />
    <xsl:variable name="extensionJPG" select=" '.jpg' " />
    <h3><font color="#bb0000">Principal component analysis of the criteria correlation index</font></h3>
    <div style="text-align: left;">	
      <p><a href="{concat($path,$name,$extensionPDF)}" >
      See PDF graphic file for better image quality and zooming options</a>
        (generated with R).</p>
      <img src="{concat($path,$name,$extensionJPG)}"  />
    </div> 
    
  </xsl:template>
  
  <xsl:template match="alternativesComparisons[@mcdaConcept='Vetoes']" >
         <a name="vetos" />
        <xsl:apply-templates mode="veto"/>
  </xsl:template>
  
  <xsl:template match="valuation" mode="bipolar">
       <xsl:apply-templates select="description"/>
       <xsl:variable name="median" select="quantitative/minimum + (quantitative/maximum - quantitative/minimum) div 2"></xsl:variable>
       <table cellpadding="1" border="1">
         <tr><td bgcolor="#FFF79B">Maximum</td><td bgcolor="#ddffdd" align="right"><xsl:value-of select="format-number(quantitative/maximum,'#.##')"/></td></tr>
         <tr><td bgcolor="#FFF79B">Median</td><td bgcolor="#dddddd"  align="right"><xsl:value-of select="format-number($median,'#.##')" /></td></tr>
         <tr><td bgcolor="#FFF79B">Minimum</td><td bgcolor="#ffddff"  align="right"><xsl:value-of select="format-number(quantitative/minimum,'#.##')"/></td></tr>
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
    <!-- nothing -->
  </xsl:template>
 
  <xsl:template match="comparisonType" mode="bipolar">
    <!-- nothing -->
  </xsl:template>
 
 
  <xsl:template match="pairs" mode="veto">
       <xsl:variable name="Veto" select='.' />
       <xsl:apply-templates select="description"/>
    <p>(The <b>concordance degree</b> of an outranking statement (an arc) results from the 
      difference between the significance (the sum of weights) of the coalition of criteria 
      in favour and the significance of the coalition of criteria in disfavour of this statement.)</p>
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
    <xsl:apply-templates select="description"/>

    <table border="1">
      <tr bgcolor="#9acd32">
        <th>relation</th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
      <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
                   <xsl:variable name="currentRow" select='@id' />
       <tr>
        <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
         <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
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
    <xsl:apply-templates select="description"/>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th><xsl:value-of select="parent::node()/description/name"/></th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
        <xsl:variable name="Min" select="parent::node()/valuation/quantitative/minimum"/>
        <xsl:variable name="Max" select="parent::node()/valuation/quantitative/maximum"/>
        <xsl:variable name="Med" select="$Min + ($Max - $Min) div 2"/>

      
      <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
        <xsl:variable name="currentRow" select='@id' />
        <tr>
          <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
          <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
            <xsl:variable name="currentColumn" select='@id' />
            <xsl:for-each select="$currentArcs/pair[initial/alternativeID=$currentRow]">
              <xsl:variable name="currentArc" select="."/>
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
            <xsl:for-each select="$currentArcs/pair[initial/criterionID=$currentRow]">
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
  
  <xsl:template name="currentValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
    <xsl:if test="$currentArc/initial/alternativeID=$currentRow">
      <xsl:if test="$currentArc/terminal/alternativeID=$currentColumn">
        <td align="right" ><xsl:value-of select="./value"/></td>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="currentBipolarValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
      <xsl:param name="Med"/>
    <xsl:if test="$currentArc/initial/alternativeID=$currentRow">
      <xsl:if test="$currentArc/terminal/alternativeID=$currentColumn">
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
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='ind']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakPreference']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='pref']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakVeto']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='veto']/."/></td></tr>
     </xsl:for-each>
   </table>
   
</xsl:template>

<xsl:template match="function/constant">
  <!--<xsl:if test="descendant::*name()= 'linear'">integer<xsl:value-of select="."/></xsl:if>
  <xsl:value-of select="."/> -->
  <xsl:apply-templates/>
</xsl:template>

  <xsl:template match="constant">
  <!--<xsl:if test="descendant::*name()= 'linear'">integer<xsl:value-of select="."/></xsl:if>
  <xsl:value-of select="."/> -->
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="value/integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>
<xsl:template match="integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>

<xsl:template match="value[real]">
  <xsl:value-of select="format-number(.,'0.00')"/>
</xsl:template>

  <xsl:template match="real">
  <xsl:value-of select="format-number(.,'0.00')"/>
</xsl:template>

  <xsl:template match="value/rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>
<xsl:template match="rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>


<xsl:template match="function[linear]">
  <xsl:value-of select="intercept/."/> + <xsl:value-of select="slope/."/>x
</xsl:template>
<xsl:template match="linear">
  <xsl:value-of select="intercept/."/> + <xsl:value-of select="slope/."/>x
</xsl:template>



  <!-- Controlling the presentation criteria X alternatives of the performance table -->
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
          <xsl:with-param name="currentAlternative" select="$currentAlternative">
          </xsl:with-param>
          <xsl:with-param name="currentCriterion" select="$currentCriterion"></xsl:with-param>
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
  
  <xsl:key name="currentAlternative" match="/xmcda:XMCDA/alternatives/alternative" use='.'  />
  
  <xsl:variable name="allAlternatives" 
    select="/xmcda:XMCDA/alternatives/alternative[
    generate-id() = 
    generate-id(key('currentAlternative',.)[1] 
    )
    ]" />  
  
  
<xsl:template match="performanceTable" mode="criterionEvaluations" >
  <a name="performance" />
   <xsl:variable name="currentTable" select="."></xsl:variable>
    <xsl:apply-templates  select="description"/>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>criterion</th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
	  <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      <xsl:apply-templates select="$currentTable/criterionEvaluations"/> 
    </table>
</xsl:template>

<xsl:template match="criterionEvaluations">
  <tr>
    <th bgcolor="#FFF79B"><xsl:value-of select="criterionID"/></th>
    <xsl:variable name="currentCriterion" select="."></xsl:variable>
    <xsl:for-each select="key('currentAlternative', $allAlternatives)">
      <xsl:variable name="currentAlternative" select="./@id"></xsl:variable>
       <xsl:call-template name="performanceRowCritEval">
         <xsl:with-param name="currentCriterion" select="$currentCriterion">
         </xsl:with-param>
         <xsl:with-param name="currentAlternative" select="$currentAlternative"></xsl:with-param>
       </xsl:call-template>
      </xsl:for-each>
  </tr>
</xsl:template>

<xsl:template name="performanceRowCritEval">
      <xsl:param name="currentCriterion"></xsl:param>
      <xsl:param name="currentAlternative"></xsl:param>
      <xsl:variable name="currentPerformance" select="$currentCriterion/evaluation[alternativeID=$currentAlternative]"></xsl:variable>
     <td align="right"><xsl:apply-templates select="$currentPerformance/value"/></td>
</xsl:template>


  <xsl:template match="XMCDA/alternatives/description">
  <!-- no comments -->
</xsl:template>

  <!-- Presenting Choice Recommendation -->
<xsl:template match="alternativesSets[@mcdaConcept='goodChoices']">
    <a name="choice"></a>
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
   <xsl:for-each select="alternativesSet[@mcdaConcept='goodChoice']">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B">{
           <xsl:for-each select="element">
             <xsl:value-of select="./alternativeID"/>,
           </xsl:for-each>}
           </th>
           <td align="center"><xsl:value-of select="values/value[@name='determinateness']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranking']"/></td>
         <td align="center"><xsl:value-of select="values/value[@name='outranked']"/></td>
         <td><xsl:value-of select="description/comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>
 
  <xsl:template match="alternativesSets[@mcdaConcept='badChoices']">
    <a name="choice"></a>
   <xsl:apply-templates  select="description"/>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Choice set</th>
        <th>Determinateness</th>
        <th>Outrankedness</th>
        <th>Outrankingness</th>
        <th>Comment</th>
      </tr>
     <xsl:for-each select="alternativesSet[@mcdaConcept='badChoice']">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#add8e6">{
           <xsl:for-each select="element">
             <xsl:value-of select="./alternativeID"/>,
           </xsl:for-each>}
           </th>
           <td align="center"><xsl:value-of select="values/value[@name='determinateness']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranked']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranking']"/></td>
           <td><xsl:value-of select="description/comment"/></td>
	  </tr>
   </xsl:for-each>
   </table>
</xsl:template>
 
</xsl:stylesheet>
    """

robustRubisXSL =\
"""<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                       xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">
  
<!-- 
XMCDA 2.0 Rubis XSLT tranformation to HTML, RB 2009
$Revision: 1.5 $
The ressource comes with ABSOLUTELY NO WARRANTY 
to the extent permitted by the applicable law.
This is free software, and you are welcome to 
redistribute it if it remains free software. 
Copyright (C) 2009 DECISION DECK Consortium
-->


 <!-- Main start of the transform -->
  
<xsl:template match="/" >
 <html>
  <head><title>Decision-Deck UMCDA-ML application</title></head>
  <body>
    <h1><font color="#0000bb">Decision-Deck UMCDA-ML Application</font></h1>

    <xsl:apply-templates  select="xmcda:XMCDA" />
    <br/>
    <h2>Content</h2>
    <ul>
      <li><a href="#choice">Choice Recommendation</a></li>
      <li><a href="#graph">Robustly significant outranking digraph</a></li>
      <li><a href="#alternatives">Potential decision actions</a></li>
      <li><a href="#performance">Performance table</a></li>
      <li><a href="#objectives">Decision objectives</a></li>
      <li><a href="#criteria">Family of criteria</a></li>
      <li><a href="#outranking">Condorcet robustness denotation</a></li>	
      <li><a href="#vetos">Veto situations</a></li>	
      <li><a href="#notice">Notice</a></li>	
    </ul>
    <hr />
    <h2><a name="notice"><font color="#bb0000">Notice</font></a></h2>
    <p>Bisdorff R., Meyer P., Roubens M., <b>Rubis</b>: A new methodology for the choice decision problem. 4OR, 
      <em>A Quarterly Journal of Operational Research</em>, Springer (2008), Vol 6 Number 2 pp. 143-165, DOI 10.1007/s10288-007-0045-5.
    <a href="http://sma.uni.lu/bisdorff/documents/HyperKernels.pdf">PDF preprint version</a>.</p>
   <p>Online documentation: <a href="https://www.decision-deck.org/project/">Decision Deck Project</a><br/>
     <b>Rubis XSL Transformation to HTML</b> R. Bisdorff, $Revision: 1.5 $<br/>
          <a href="http://www.decision-deck.org/xmcda">XMCDA 2.0 Schema</a> P. Meyer and Th. Veneziano 2009 <br/>
           Copyright © 2009 DECISION DECK Consortium</p>
   </body>
  </html>
</xsl:template>
 

 <!--  generic description layout: must fit all element description !!! -->
  
  <xsl:template match="projectReference">
     <xsl:apply-templates />
    <h3>Content</h3>
    <ul>
      <li><a href="#choice">Choice Recommendation</a></li>
      <li><a href="#graph">Robustly significant outranking digraph</a></li>
      <li><a href="#alternatives">Potential decision actions</a></li>
      <li><a href="#performance">Performance table</a></li>
      <li><a href="#objectives">Decision objectives</a></li>
      <li><a href="#criteria">Family of criteria</a></li>
      <li><a href="#outranking">Condorcet robustness denotation</a></li>	
      <li><a href="#vetos">Veto situations</a></li>	
      <li><a href="#notice">Notice</a></li>	
    </ul>
  </xsl:template>
  
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
    <h2><font color="#bb0000"><xsl:value-of select="text()"/></font></h2>
  </xsl:template>
  
  <xsl:template match="subTitle">
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
    Comment: <em><xsl:value-of select="text()" /></em><br/>
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

<!--  Method Options  -->

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

<!-- List of potential alternatives -->
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

  <!-- relation on Alternatives -->
  <xsl:template match="alternativesComparisons[@mcdaConcept='CondorcetRobustness']">
    <h2><a name="graph"><font color="#bb0000">Robustly Concordant Outranking Graph</font></a></h2>
    <p>(<i><b> Black arrows</b> indicate outranking situations supported by a criteria coalition 
      of positive significance, i.e. gathering more than 50&#37; of the global criteria significance weights.
      <b>Empty arrow heads</b> indicate an indeterminate outranking situation.</i>)</p>
    <xsl:variable name="tiret" select=" '-' " />
    <xsl:variable name="dot" select=" '.' " />
    <xsl:variable name="name" select ="/xmcda:XMCDA/@instanceID" />
    <xsl:variable name="path" select=" 'rubisGraph-' " />
    <xsl:variable name="extensionPNG" select=" '.png' " />
    <xsl:variable name="extensionPDF" select=" '.pdf' " />
    <div style="text-align: left;">	
      <p><a href="{concat($path,$name,$extensionPDF)}" >
      See PDF graphic file for better image quality and zooming options</a>
        (generated with GraphViz).</p> 
      <img src="{concat($path,$name,$extensionPNG)}"  />   
    </div> 
    
    <a name="outranking"/>
    <xsl:choose>
      <xsl:when test="valuation/valuationType='bipolar'">
        <xsl:apply-templates mode="bipolar"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
 
  <xsl:template match="criteriaComparisons[@mcdaConcept='correlationTable']">
    <a name="correlation"/>
    <xsl:apply-templates mode="simil"/>
    <xsl:variable name="tiret" select=" '-' " />
    <xsl:variable name="dot" select=" '.' " />
    <xsl:variable name="name" select ="/xmcda:XMCDA/@instanceID" />
    <xsl:variable name="path" select=" 'similarityPlot-' " />
    <xsl:variable name="extensionPDF" select=" '.pdf' " />
    <xsl:variable name="extensionJPG" select=" '.jpg' " />
    <h3><font color="#bb0000">Principal component analysis of the criteria correlation index</font></h3>
    <div style="text-align: left;">	
      <p><a href="{concat($path,$name,$extensionPDF)}" >
      See PDF graphic file for better image quality and zooming options</a>
        (generated with R).</p>
      <img src="{concat($path,$name,$extensionJPG)}"  />
    </div> 
    
  </xsl:template>
  
  <xsl:template match="alternativesComparisons[@mcdaConcept='Vetoes']" >
         <a name="vetos" />
        <xsl:apply-templates mode="veto"/>
  </xsl:template>
  
  <xsl:template match="valuation" mode="bipolar">
    <xsl:apply-templates select="description"/>
    <table cellpadding="1" border="1">
      <tr><td bgcolor="#FFF79B">Unanimously concordant</td> <td align="right" bgcolor="#78ff78"> <xsl:value-of select="quantitative/maximum"/></td></tr>
      <tr><td bgcolor="#FFF79B">Ordinal majority concordant</td> <td align="right" bgcolor="#bdffbd"> 2</td></tr>
      <tr><td bgcolor="#FFF79B">Cardinal majority concordant</td> <td align="right" bgcolor="#e6ffe6"> 1</td></tr>
      <tr><td bgcolor="#FFF79B">Balanced concordance and discordance, or weak veto</td> <td align="right" bgcolor="#ffffff" > 0</td></tr>
      <tr><td bgcolor="#FFF79B">Simple majority discordant</td> <td align="right" bgcolor="#fff0ff" >-1</td></tr>
      <tr><td bgcolor="#FFF79B">Ordinal majority discordant</td> <td align="right" bgcolor="#ffd4ff" >-2</td></tr>
      <tr><td bgcolor="#FFF79B">Unanimously discordant, or veto</td> <td align="right" bgcolor="#ffadff" ><xsl:value-of select="quantitative/minimum"/></td></tr>
    </table>
  </xsl:template>
  
  <!--<xsl:template match="valuation" mode="bipolar">
       <xsl:apply-templates select="description"/>
       <xsl:variable name="median" select="quantitative/minimum + (quantitative/maximum - quantitative/minimum) div 2"></xsl:variable>
       <table cellpadding="1" border="1">
         <tr><td bgcolor="#FFF79B">Maximum</td><td bgcolor="#ddffdd" align="right"><xsl:value-of select="format-number(quantitative/maximum,'#.##')"/></td></tr>
         <tr><td bgcolor="#FFF79B">Median</td><td bgcolor="#dddddd"  align="right"><xsl:value-of select="format-number($median,'#.##')" /></td></tr>
         <tr><td bgcolor="#FFF79B">Minimum</td><td bgcolor="#ffddff"  align="right"><xsl:value-of select="format-number(quantitative/minimum,'#.##')"/></td></tr>
       </table>
    
  </xsl:template>
   -->
  <xsl:template match="valuation">
       <xsl:apply-templates select="description"/>
        <table cellpadding="1" border="1">
         <tr><td bgcolor="#FFF79B">Minimum</td><td align="right"><xsl:value-of select="quantitative/minimum"/></td></tr>
         <tr><td bgcolor="#FFF79B">Maximum</td><td align="right"><xsl:value-of select="quantitative/maximum"/></td></tr>
        </table>
  </xsl:template>
 
 <xsl:template match="comparisonType">
    <!-- nothing -->
  </xsl:template>
 
  <xsl:template match="comparisonType" mode="bipolar">
    <!-- nothing -->
  </xsl:template>
 
 
  <xsl:template match="pairs" mode="veto">
       <xsl:variable name="Veto" select='.' />
       <xsl:apply-templates select="description"/>
    <p>(The <b>concordance degree</b> of an outranking statement (an arc) results from the 
      difference between the significance (the sum of weights) of the coalition of criteria 
      in favour and the significance of the coalition of criteria in disfavour of this statement.)</p>
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
    <xsl:apply-templates select="description"/>

    <table border="1">
      <tr bgcolor="#9acd32">
        <th>relation</th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
      <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
                   <xsl:variable name="currentRow" select='@id' />
       <tr>
        <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
         <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
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
    <xsl:apply-templates select="description"/>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th><xsl:value-of select="parent::node()/description/name"/></th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
          <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      
        <xsl:variable name="Min" select="parent::node()/valuation/quantitative/minimum"/>
        <xsl:variable name="Max" select="parent::node()/valuation/quantitative/maximum"/>
        <xsl:variable name="Med" select="$Min + ($Max - $Min) div 2"/>

      
      <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
        <xsl:variable name="currentRow" select='@id' />
        <tr>
          <th bgcolor="#FFF79B"><xsl:value-of select="$currentRow"/></th>
          <xsl:for-each select="/xmcda:XMCDA/alternatives[@mcdaConcept='alternatives']/alternative">
            <xsl:variable name="currentColumn" select='@id' />
            <xsl:for-each select="$currentArcs/pair[initial/alternativeID=$currentRow]">
              <xsl:variable name="currentArc" select="."/>
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
            <xsl:for-each select="$currentArcs/pair[initial/criterionID=$currentRow]">
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
  
  <xsl:template name="currentValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
    <xsl:if test="$currentArc/initial/alternativeID=$currentRow">
      <xsl:if test="$currentArc/terminal/alternativeID=$currentColumn">
        <td align="right" ><xsl:value-of select="./value"/></td>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="currentBipolarValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
    <xsl:param name="Med"/>
    <xsl:if test="$currentArc/initial/alternativeID=$currentRow">
      <xsl:if test="$currentArc/terminal/alternativeID=$currentColumn">
        <xsl:variable name="arcValue" select="$currentArc/values/value[@name='outranking']"></xsl:variable>
        <xsl:variable name="arcRobustness" select="$currentArc/values/value[@name='robustness']"></xsl:variable>
       <xsl:choose>
          <xsl:when test="$arcRobustness = 3">
            <td bgcolor="#78ff78" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
            <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
          </xsl:when>
         <xsl:when test="$arcRobustness = 2">
            <td bgcolor="#bdffbd" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
           <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
         </xsl:when>
         <xsl:when test="$arcRobustness = 1">
            <td bgcolor="#e6ffe6" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
           <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
         </xsl:when>
         <xsl:when test="$arcRobustness = -3">
            <td bgcolor="#ffadff" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
           <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
         </xsl:when>
         <xsl:when test="$arcRobustness = -2">
            <td bgcolor="#ffd4ff" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
           <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
         </xsl:when>
         <xsl:when test="$arcRobustness = -1">
            <td bgcolor="#fff0ff" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
           <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
         </xsl:when>
          <xsl:otherwise>
            <td bgcolor="#ffffff" align="right" >
              <!--<xsl:value-of select="$arcRobustness"/> (<xsl:value-of select="$arcValue"/>)</td>-->
            <xsl:value-of select="$arcValue"/> (<xsl:value-of select="$arcRobustness"/>)</td>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
<!--  <xsl:template name="currentBipolarValue" match="pair">
    <xsl:param name="currentRow"/>
    <xsl:param name="currentColumn"/>
    <xsl:param name="currentArc"/>
      <xsl:param name="Med"/>
    <xsl:if test="$currentArc/initial/alternativeID=$currentRow">
      <xsl:if test="$currentArc/terminal/alternativeID=$currentColumn">
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
-->
  
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
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='ind']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakPreference']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='pref']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='weakVeto']/."/></td>
         <td align="center"><xsl:apply-templates select="thresholds/threshold[@id='veto']/."/></td></tr>
     </xsl:for-each>
   </table>
   
</xsl:template>

<xsl:template match="function/constant">
  <!--<xsl:if test="descendant::*name()= 'linear'">integer<xsl:value-of select="."/></xsl:if>
  <xsl:value-of select="."/> -->
  <xsl:apply-templates/>
</xsl:template>

  <xsl:template match="constant">
  <!--<xsl:if test="descendant::*name()= 'linear'">integer<xsl:value-of select="."/></xsl:if>
  <xsl:value-of select="."/> -->
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="value/integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>
<xsl:template match="integer">
  <xsl:value-of select="format-number(.,'#')" />
</xsl:template>

<xsl:template match="value[real]">
  <xsl:value-of select="format-number(.,'0.00')"/>
</xsl:template>

  <xsl:template match="real">
  <xsl:value-of select="format-number(.,'0.00')"/>
</xsl:template>

  <xsl:template match="value/rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>
<xsl:template match="rational">
  <xsl:value-of select="//numerator" /> <xsl.text>/</xsl.text><xsl:value-of select="//denominator"/>
</xsl:template>


<xsl:template match="function[linear]">
  <xsl:value-of select="intercept/."/> + <xsl:value-of select="slope/."/>x
</xsl:template>
<xsl:template match="linear">
  <xsl:value-of select="intercept/."/> + <xsl:value-of select="slope/."/>x
</xsl:template>



  <!-- Controlling the presentation criteria X alternatives of the performance table -->
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
          <xsl:with-param name="currentAlternative" select="$currentAlternative">
          </xsl:with-param>
          <xsl:with-param name="currentCriterion" select="$currentCriterion"></xsl:with-param>
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
  
  <xsl:key name="currentAlternative" match="/xmcda:XMCDA/alternatives/alternative" use='.'  />
  
  <xsl:variable name="allAlternatives" 
    select="/xmcda:XMCDA/alternatives/alternative[
    generate-id() = 
    generate-id(key('currentAlternative',.)[1] 
    )
    ]" />  
  
  
<xsl:template match="performanceTable" mode="criterionEvaluations" >
  <a name="performance" />
   <xsl:variable name="currentTable" select="."></xsl:variable>
    <xsl:apply-templates  select="description"/>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>criterion</th>
        <xsl:for-each select="/xmcda:XMCDA/alternatives/alternative">
	  <th bgcolor="#FFF79B"><xsl:value-of select="@id"/></th>
        </xsl:for-each>
      </tr>
      <xsl:apply-templates select="$currentTable/criterionEvaluations"/> 
    </table>
</xsl:template>

<xsl:template match="criterionEvaluations">
  <tr>
    <th bgcolor="#FFF79B"><xsl:value-of select="criterionID"/></th>
    <xsl:variable name="currentCriterion" select="."></xsl:variable>
    <xsl:for-each select="key('currentAlternative', $allAlternatives)">
      <xsl:variable name="currentAlternative" select="./@id"></xsl:variable>
       <xsl:call-template name="performanceRowCritEval">
         <xsl:with-param name="currentCriterion" select="$currentCriterion">
         </xsl:with-param>
         <xsl:with-param name="currentAlternative" select="$currentAlternative"></xsl:with-param>
       </xsl:call-template>
      </xsl:for-each>
  </tr>
</xsl:template>

<xsl:template name="performanceRowCritEval">
      <xsl:param name="currentCriterion"></xsl:param>
      <xsl:param name="currentAlternative"></xsl:param>
      <xsl:variable name="currentPerformance" select="$currentCriterion/evaluation[alternativeID=$currentAlternative]"></xsl:variable>
     <td align="right"><xsl:apply-templates select="$currentPerformance/value"/></td>
</xsl:template>


  <xsl:template match="XMCDA/alternatives/description">
  <!-- no comments -->
</xsl:template>

  <!-- Presenting Choice Recommendation -->
<xsl:template match="alternativesSets[@mcdaConcept='goodChoices']">
    <a name="choice"></a>
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
   <xsl:for-each select="alternativesSet[@mcdaConcept='goodChoice']">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#FFF79B">{
           <xsl:for-each select="element">
             <xsl:value-of select="./alternativeID"/>,
           </xsl:for-each>}
           </th>
           <td align="center"><xsl:value-of select="values/value[@name='determinateness']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranking']"/></td>
         <td align="center"><xsl:value-of select="values/value[@name='outranked']"/></td>
         <td><xsl:value-of select="description/comment"/></td>
	</tr>
   </xsl:for-each>
   </table>
</xsl:template>
 
  <xsl:template match="alternativesSets[@mcdaConcept='badChoices']">
    <a name="choice"></a>
   <xsl:apply-templates  select="description"/>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>#</th>
        <th>Choice set</th>
        <th>Determinateness</th>
        <th>Outrankedness</th>
        <th>Outrankingness</th>
        <th>Comment</th>
      </tr>
     <xsl:for-each select="alternativesSet[@mcdaConcept='badChoice']">
       <tr><td><xsl:number format="1"/></td>
         <th bgcolor="#add8e6">{
           <xsl:for-each select="element">
             <xsl:value-of select="./alternativeID"/>,
           </xsl:for-each>}
           </th>
           <td align="center"><xsl:value-of select="values/value[@name='determinateness']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranked']"/></td>
           <td align="center"><xsl:value-of select="values/value[@name='outranking']"/></td>
           <td><xsl:value-of select="description/comment"/></td>
	  </tr>
   </xsl:for-each>
   </table>
</xsl:template>
 
</xsl:stylesheet>
    """

def saveRubisXSL(fileName='xmcda2Rubis.xsl',Extended=True):
    """
    Save the standard Rubis XMCDA 2.0 XSL style sheet in the current working directory.
    This style sheet allows to visualize an XMCDA 2.0 encoded performance tableau in a browser.

    .. note::

        When accessing an XMCDA encoded data file in a browser, for safety reasons, the corresponding XSL style sheet
        must be present in the same working directory.
    
    """
    import xmcda
    fo = open(fileName,'w')
    if Extended:
        fo.write(xmcda.rubisExtXSL)
    else:
        fo.write(xmcda.rubisXSL)
    fo.close()

def saveRubisChoiceXSL(fileName='xmcda2RubisChoice.xsl'):
    """
    Save the local Rubis Best-Choice XMCDA 2.0 XSL style sheet in the current working directory
    This style sheet allows to browse an XMCDA 2.0 encoded Rubis Best-Choice recommendation.

    .. note::

        When accessing an XMCDA encoded data file in a browser, for safety reasons, the corresponding XSL style sheet
        must be present in the same working directory.
      
    """
    import xmcda
    fo = open(fileName,'w')
    fo.write(xmcda.rubisChoiceXSL)
    fo.close()

def saveRobustRubisChoiceXSL(fileName='xmcda2RubisRobustChoice.xsl'):
    """
    Save the robust version of the Rubis Best-Choice XMCDA 2.0 XSL style sheet in the current working directory
    This style sheet allows to browse an XMCDA 2.0 encoded robust Rubis Best-Choice recommendation.

    .. note::

        When accessing an XMCDA encoded data file in a browser, for safety reasons, the corresponding XSL style sheet
        must be present in the same working directory.
    
    """
    import xmcda
    fo = open(fileName,'w')
    fo.write(xmcda.robustRubisXSL)
    fo.close()

def saveXMCDARubisBestChoiceRecommendation(problemFileName=None,tempDir='.',valuationType=None):
    """
    Store an XMCDA2 encoded solution file of the Rubis best-choice recommendation.

      The valuationType parameter allows to work:
    
        - on the standard bipolar outranking digraph (valuationType = 'bipolar', default),
        - on the normalized --[-1,1] valued-- bipolar outranking digraph (valuationType = 'normalized'),
        - on the robust --ordinal criteria weights-- bipolar outranking digraph (valuationType = 'robust'),
        - on the confident outranking digraph (valuationType = 'confident'),
        - ignoring considerable performances differences (valuationType = 'noVeto').  

    .. note::

         The method requires an Unix like OS like Ubuntu or Mac OSX and depends on:

              - the R statistics package for Principal Component Analysis graphic,
              - the C calmat matrix interpreter (On http://leopold-loewenheim.uni.lu/svn/repos/Calmat/  see README)
              - the xpdf ressources ( ...$ apt-get install xpdf on Ubuntu) for converting pdf files to ppm format, and ppm files to png format.  
        
    """
    from xml.etree import ElementTree
    import os, copy, xmcda
    from sys import platform
    from outrankingDigraphs import BipolarOutrankingDigraph,\
         ConfidentBipolarOutrankingDigraph, RobustOutrankingDigraph
    
    
    def errorExit(tempDir,problemFileName,Number,Name,Message):
        """
        XMCDA 2.0 Error message
        """
        #print(tempDir,problemFileName,Number,Name,Message)
        solutionFileName = str(tempDir)+'/solution-' + str(problemFileName) + '.xmcda2'
        fo = open(solutionFileName,'w')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2008/XMCDA-2.0.0 file:../XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">'))
        # write error message
        fo.write('<methodMessages>\n')
        fo.write('<description>\n')
        fo.write('<title>XMCDA 2.0 Error Messages</title>\n')
        fo.write('</description>\n')
        fo.write('<errorMessage name="%s">\n' % (Name) )
        fo.write('<number>%d</number>\n' % (Number) )
        fo.write('<text>%s</text>\n' % (Message) )
        fo.write('</errorMessage>\n')
        fo.write('</methodMessages>\n')
        fo.write('</xmcda:XMCDA>\n')
        fo.close()
        return Number
        #exit(Number)


    if problemFileName == None:
        errorExit(tempDir,problemFileName, 1, 'Input error', 'No data file name given !')
        return

    #########   main #################
    # get XML file type and load problem data
    try:
            problemFileNameExt = problemFileName+'.xml'
            fo = codecs.open(problemFileNameExt,mode='r',encoding='utf-8')
            rootTag = ElementTree.parse(fo).getroot().tag 
            fo.close()
    except:
            try:
                    problemFileNameExt = problemFileName+'.xmcda2'
                    fo = codecs.open(problemFileNameExt,mode='r',encoding='utf-8')
                    rootTag = ElementTree.parse(fo).getroot().tag
                    fo.close()
            except:
                    problemFileNameExt = problemFileName+'.xmcda'
                    fo = codecs.open(problemFileNameExt,mode='r',encoding='utf-8')
                    rootTag = ElementTree.parse(fo).getroot().tag
                    fo.close()

##    try:
##        t = XMCDA2PerformanceTableau(problemFileName)
##        
##    except:
##        errorExit(tempDir,problemFileName, 1, 'UMCDA-ML XMCDA 2.0 input error', 'Error when reading XML input data file !')
##        return
        


    if rootTag == 'RubisPerformanceTableau':
        try:
            t = XMLRubisPerformanceTableau(problemFileName)
        except:
            errorExit(tempDir,problemFileName, 1, 'Rubis XML input error', 'Error when reading XML input data file !')
            return
    elif rootTag == '{http://www.decision-deck.org/2009/XMCDA-2.0.0}XMCDA':
        try:
            t = XMCDA2PerformanceTableau(problemFileName)
        except:
            errorExit(tempDir,problemFileName, 1, 'UMCDA-ML XMCDA 2.0 input error', 'Error when reading XML input data file !')
            return
    elif rootTag == '{http://www.decision-deck.org/2008/UMCDA-ML-1.0}XMCDA':
        try:
            t = XMCDAPerformanceTableau(problemFileName)
        except:
            errorExit(tempDir,problemFileName, 1, 'UMCDA-ML XMCDA 1.0 input error', 'Error when reading XML input data file !')
            return
    else:
        errorExit(tempDir,problemFileName, 1, 'Input error', 'Error when reading input data file !')
        return

##    t = XMCDA2PerformanceTableau(problemFileName)
##    print(rootTag,t)
    

    # contruct outranking digraph
    isRobust = False
    #print(isRobust)
    if valuationType == None:
        try:
            if rootTag != 'rubisPerformanceTableau':
                if t.parameter['valuationType'] == 'integer':
                    g = BipolarIntegerOutrankingDigraph(t)
##                elif t.parameter['valuationType'] == 'electre3':
##                    g = Electre3OutrankingDigraph(t)
                elif t.parameter['valuationType'] == 'normalized':
                    g = BipolarOutrankingDigraph(t)
                    g.recodeValuation(-1.0,1.0)
                elif t.parameter['valuationType'] == 'bipolar':
                    g = BipolarOutrankingDigraph(t,hasBipolarVeto=True)
                elif t.parameter['valuationType'] == 'confident':
                    g = ConfidentBipolarOutrankingDigraph(t,hasBipolarVeto=True)
##                elif t.parameter['valuationType'] == 'electreVeto':
##                    g = BipolarOutrankingDigraph(t,hasBipolarVeto=False)
                elif t.parameter['valuationType'] == 'noVeto':
                    g = BipolarOutrankingDigraph(t,hasNoVeto=True)
                elif t.parameter['valuationType'] == 'robust':
                    g = RobustOutrankingDigraph(t)
                    isRobust = True			
            else:
                g = BipolarOutrankingDigraph(t)
                #print(g)
        except:
            errorExit(tempDir,problemFileName, 2, 'Corrupt problem data', 'Error when computing outranking digraph !')
            return
    elif valuationType == 'robust':
        g = RobustOutrankingDigraph(t)
        isRobust = True
    elif valuationType == 'confident':
        g = ConfidentBipolarOutrankingDigraph(t)
    elif valuationType == 'noVeto':
        g = BipolarOutrankingDigraph(t,hasNoVeto=True)
    else:
        g = BipolarOutrankingDigraph(t)

##    g = BipolarOutrankingDigraph(t)
##    print(g)

    # save Rubis solution file
    g_orig = copy.deepcopy(g)
    solutionFileName = str(tempDir)+'/solution-' + str(problemFileName)
    try:
        g.saveXMCDA2RubisChoiceRecommendation(\
            fileName=solutionFileName,author='XMCDA 2.0 Rubis Server',\
            servingD3=False,comment=True,instanceID=problemFileName)
    except:
        errorExit(tempDir,problemFileName, 3, 'Rubis Solver error', 'Error when computing Rubis choice recommendation !')
        return

    g_orig.goodChoices=[]
    try:
        for ch in g.goodChoices[0][5]:
            if isinstance(ch,frozenset):
                for x in ch:
                    g_orig.goodChoices.append(x)
            else:
                g_orig.goodChoices.append(ch)
    except:
        pass

    g_orig.badChoices=[]
    try:
        for ch in g.badChoices[0][5]:
            if isinstance(ch,frozenset):
                for x in ch:
                    g_orig.badChoices.append(x)
            else:
                g_orig.badChoices.append(ch)
    except:
        pass	

    graphFileName = str(tempDir)+'/rubisGraph-' + str(problemFileName)
    try:
        g_orig.exportGraphViz(\
            fileName=graphFileName,\
            bestChoice=g_orig.goodChoices,\
            worstChoice=g_orig.badChoices,\
            Comments=True,graphType='png',graphSize='10,10')
        g_orig.exportGraphViz(\
                                  fileName=graphFileName,bestChoice=g_orig.goodChoices,\
                                  worstChoice=g_orig.badChoices,Comments=False,\
                                  graphType='pdf',graphSize='10,10')
    except: 
        errorExit(tempDir,problemFileName, 4, 'GraphViz export error', 'Error when computing the outranking digraph image.')
        return

    # criteria correlation

    #similarityPlotFileName = str(tempDir)+'/similarityPlot-' + str(problemFileName)
    similarityPlotFileName = problemFileName
    try:
        if not isRobust:
            g_orig.export3DplotOfCriteriaCorrelation(plotFileName=similarityPlotFileName,Type="pdf",Comments=True,bipolarFlag=True,dist=False,centeredFlag=True)
    except:
        errorExit(tempDir,problemFileName,5, 'Calmat or R error', 'Error when generating the criteria correlation png plot.')
        return

    # copy similarity jpg in place
    if not isRobust:
        inFile = similarityPlotFileName + '.pdf'
        import os.path
        if os.path.isfile(inFile):
            outFile = str(tempDir)+'/similarityPlot-' + str(problemFileName)+'.jpg'
            if platform == 'darwin':
                commandString = 'pdftoppm -r 85 %s %s/temp ; ppmtojpeg %s/temp-000001.ppm > %s/temp.jpg; cp %s/temp.jpg %s' % ( inFile,str(tempDir),str(tempDir),str(tempDir),str(tempDir),outFile)
            else:
                commandString = 'pdftoppm -r 85 < ' + inFile + ' > /tmp/temp.ppm ; ppmtojpeg < /tmp/temp.ppm > /tmp/temp.jpg; cp /tmp/temp.jpg ' + outFile
            try:
                os.system(commandString)
            except:
                errorExit(tempDir,problemFileName,6, 'system error', 'Error when generating the criteria correlation jpeg plot.')
                return

    # copy Rubis styles sheet
    xmcda.saveRubisXSL(str(tempDir)+'/xmcda2Rubis.xsl')
    if isRobust:
        xmcda.saveRobustRubisChoiceXSL(str(tempDir)+'/xmcda2RubisRobustChoice.xsl')
    else:
        xmcda.saveRubisChoiceXSL(str(tempDir)+'/xmcda2RubisChoice.xsl')

def showXMCDARubisBestChoiceRecommendation(problemFileName=None,valuationType=None):
    """
    Launches a browser window with the XMCDA2 solution of the
    Rubis Solver computed from a stored XMCDA2 encoded performance tableau.

    The valuationType parameter allows to work:
    
        - on the standard bipolar outranking digraph (valuationType = 'bipolar', default),
        - on the normalized --[-1,1] valued-- bipolar outranking digraph (valuationType = 'normalized'),
        - on the robust --ordinal criteria weights-- bipolar outranking digraph (valuationType = 'robust'),
        - on the confident outranking digraph (valuationType = 'confident'),
        - ignoring considerable performances differences (valuationType = 'noVeto').

    Example::

        >>> import xmcda
        >>> from randomPerfTabs import RandomCBPerformanceTableau
        >>> t = RandomCBPerformanceTableau()
        >>> t.saveXMCDA2('example')
        >>> xmcda.showXMCDARubisBestChoiceRecommendation(problemFileName='example')

    """
    
    import webbrowser, xmcda, tempfile, os
    currDir = os.getcwd()
    tempDirName = tempfile.mkdtemp(dir=currDir)
    commandString = 'cp %s.* %s' % (problemFileName,tempDirName)
    os.system(commandString)
    os.chdir(tempDirName)
    xmcda.saveXMCDARubisBestChoiceRecommendation(problemFileName,tempDirName,valuationType)
    url = tempDirName+'/solution-'+problemFileName+'.xmcda2'
    print(url)
    webbrowser.open_new('file://'+url)    
    os.chdir(currDir)
   
###############################
if __name__ == '__main__':
    ######  scratch pad for testing the module components
    from randomPerfTabs import RandomCBPerformanceTableau
    t = RandomCBPerformanceTableau(seed=10)
    t.saveXMCDA2('example')
    import xmcda
    xmcda.showXMCDARubisBestChoiceRecommendation(problemFileName='example',valuationType=None)

