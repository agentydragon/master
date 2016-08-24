import java.lang.System;
import org.junit.Test;

public class ParseXmlsToProtosTest {
	@Test
	public void testParseXmlsToProtos() throws Exception {
		String xml = ParseXmlsToProtos.readFile("testdata/Obama.txt.out");
		String plaintext = ParseXmlsToProtos.readFile("testdata/Obama.txt");
		org.w3c.dom.Document document = ParseXmlsToProtos.parseXmlFromString(xml);
		System.out.println(document);
		System.out.println(plaintext);
		Sentence.Document proto = ParseXmlsToProtos.documentToProto(document, plaintext);
		System.out.println(proto.toString());
		/*
		String str = "
<root>
  <document>
    <sentences>
      <sentence id="1">
        <tokens>
          <token id="1">
            <word>Barack</word>
            <lemma>Barack</lemma>
            <CharacterOffsetBegin>0</CharacterOffsetBegin>
            <CharacterOffsetEnd>6</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="2">
            <word>Obama</word>
            <lemma>Obama</lemma>
            <CharacterOffsetBegin>7</CharacterOffsetBegin>
            <CharacterOffsetEnd>12</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="3">
            <word>was</word>
            <lemma>be</lemma>
            <CharacterOffsetBegin>13</CharacterOffsetBegin>
            <CharacterOffsetEnd>16</CharacterOffsetEnd>
            <POS>VBD</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="4">
            <word>born</word>
            <lemma>bear</lemma>
            <CharacterOffsetBegin>17</CharacterOffsetBegin>
            <CharacterOffsetEnd>21</CharacterOffsetEnd>
            <POS>VBN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="5">
            <word>on</word>
            <lemma>on</lemma>
            <CharacterOffsetBegin>22</CharacterOffsetBegin>
            <CharacterOffsetEnd>24</CharacterOffsetEnd>
            <POS>IN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="6">
            <word>Hawaii</word>
            <lemma>Hawaii</lemma>
            <CharacterOffsetBegin>25</CharacterOffsetBegin>
            <CharacterOffsetEnd>31</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>LOCATION</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="7">
            <word>and</word>
            <lemma>and</lemma>
            <CharacterOffsetBegin>32</CharacterOffsetBegin>
            <CharacterOffsetEnd>35</CharacterOffsetEnd>
            <POS>CC</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="8">
            <word>he</word>
            <lemma>he</lemma>
            <CharacterOffsetBegin>36</CharacterOffsetBegin>
            <CharacterOffsetEnd>38</CharacterOffsetEnd>
            <POS>PRP</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="9">
            <word>is</word>
            <lemma>be</lemma>
            <CharacterOffsetBegin>39</CharacterOffsetBegin>
            <CharacterOffsetEnd>41</CharacterOffsetEnd>
            <POS>VBZ</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="10">
            <word>the</word>
            <lemma>the</lemma>
            <CharacterOffsetBegin>42</CharacterOffsetBegin>
            <CharacterOffsetEnd>45</CharacterOffsetEnd>
            <POS>DT</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="11">
            <word>president</word>
            <lemma>president</lemma>
            <CharacterOffsetBegin>46</CharacterOffsetBegin>
            <CharacterOffsetEnd>55</CharacterOffsetEnd>
            <POS>NN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="12">
            <word>of</word>
            <lemma>of</lemma>
            <CharacterOffsetBegin>56</CharacterOffsetBegin>
            <CharacterOffsetEnd>58</CharacterOffsetEnd>
            <POS>IN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="13">
            <word>the</word>
            <lemma>the</lemma>
            <CharacterOffsetBegin>59</CharacterOffsetBegin>
            <CharacterOffsetEnd>62</CharacterOffsetEnd>
            <POS>DT</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="14">
            <word>United</word>
            <lemma>United</lemma>
            <CharacterOffsetBegin>63</CharacterOffsetBegin>
            <CharacterOffsetEnd>69</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>LOCATION</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="15">
            <word>States</word>
            <lemma>States</lemma>
            <CharacterOffsetBegin>70</CharacterOffsetBegin>
            <CharacterOffsetEnd>76</CharacterOffsetEnd>
            <POS>NNPS</POS>
            <NER>LOCATION</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="16">
            <word>.</word>
            <lemma>.</lemma>
            <CharacterOffsetBegin>76</CharacterOffsetBegin>
            <CharacterOffsetEnd>77</CharacterOffsetEnd>
            <POS>.</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
        </tokens>
        <parse>(ROOT (S (S (NP (NNP Barack) (NNP Obama)) (VP (VBD was) (VP (VBN born) (PP (IN on) (NP (NNP Hawaii)))))) (CC and) (S (NP (PRP he)) (VP (VBZ is) (NP (NP (DT the) (NN president)) (PP (IN of) (NP (DT the) (NNP United) (NNPS States)))))) (. .))) </parse>
        <dependencies type="basic-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="4">born</dependent>
          </dep>
          <dep type="compound">
            <governor idx="2">Obama</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="nsubjpass">
            <governor idx="4">born</governor>
            <dependent idx="2">Obama</dependent>
          </dep>
          <dep type="auxpass">
            <governor idx="4">born</governor>
            <dependent idx="3">was</dependent>
          </dep>
          <dep type="case">
            <governor idx="6">Hawaii</governor>
            <dependent idx="5">on</dependent>
          </dep>
          <dep type="nmod">
            <governor idx="4">born</governor>
            <dependent idx="6">Hawaii</dependent>
          </dep>
          <dep type="cc">
            <governor idx="4">born</governor>
            <dependent idx="7">and</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="11">president</governor>
            <dependent idx="8">he</dependent>
          </dep>
          <dep type="cop">
            <governor idx="11">president</governor>
            <dependent idx="9">is</dependent>
          </dep>
          <dep type="det">
            <governor idx="11">president</governor>
            <dependent idx="10">the</dependent>
          </dep>
          <dep type="conj">
            <governor idx="4">born</governor>
            <dependent idx="11">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="15">States</governor>
            <dependent idx="12">of</dependent>
          </dep>
          <dep type="det">
            <governor idx="15">States</governor>
            <dependent idx="13">the</dependent>
          </dep>
          <dep type="compound">
            <governor idx="15">States</governor>
            <dependent idx="14">United</dependent>
          </dep>
          <dep type="nmod">
            <governor idx="11">president</governor>
            <dependent idx="15">States</dependent>
          </dep>
          <dep type="punct">
            <governor idx="4">born</governor>
            <dependent idx="16">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="4">born</dependent>
          </dep>
          <dep type="compound">
            <governor idx="2">Obama</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="nsubjpass">
            <governor idx="4">born</governor>
            <dependent idx="2">Obama</dependent>
          </dep>
          <dep type="auxpass">
            <governor idx="4">born</governor>
            <dependent idx="3">was</dependent>
          </dep>
          <dep type="case">
            <governor idx="6">Hawaii</governor>
            <dependent idx="5">on</dependent>
          </dep>
          <dep type="nmod:on">
            <governor idx="4">born</governor>
            <dependent idx="6">Hawaii</dependent>
          </dep>
          <dep type="cc">
            <governor idx="4">born</governor>
            <dependent idx="7">and</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="11">president</governor>
            <dependent idx="8">he</dependent>
          </dep>
          <dep type="cop">
            <governor idx="11">president</governor>
            <dependent idx="9">is</dependent>
          </dep>
          <dep type="det">
            <governor idx="11">president</governor>
            <dependent idx="10">the</dependent>
          </dep>
          <dep type="conj:and">
            <governor idx="4">born</governor>
            <dependent idx="11">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="15">States</governor>
            <dependent idx="12">of</dependent>
          </dep>
          <dep type="det">
            <governor idx="15">States</governor>
            <dependent idx="13">the</dependent>
          </dep>
          <dep type="compound">
            <governor idx="15">States</governor>
            <dependent idx="14">United</dependent>
          </dep>
          <dep type="nmod:of">
            <governor idx="11">president</governor>
            <dependent idx="15">States</dependent>
          </dep>
          <dep type="punct">
            <governor idx="4">born</governor>
            <dependent idx="16">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-ccprocessed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="4">born</dependent>
          </dep>
          <dep type="compound">
            <governor idx="2">Obama</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="nsubjpass">
            <governor idx="4">born</governor>
            <dependent idx="2">Obama</dependent>
          </dep>
          <dep type="auxpass">
            <governor idx="4">born</governor>
            <dependent idx="3">was</dependent>
          </dep>
          <dep type="case">
            <governor idx="6">Hawaii</governor>
            <dependent idx="5">on</dependent>
          </dep>
          <dep type="nmod:on">
            <governor idx="4">born</governor>
            <dependent idx="6">Hawaii</dependent>
          </dep>
          <dep type="cc">
            <governor idx="4">born</governor>
            <dependent idx="7">and</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="11">president</governor>
            <dependent idx="8">he</dependent>
          </dep>
          <dep type="cop">
            <governor idx="11">president</governor>
            <dependent idx="9">is</dependent>
          </dep>
          <dep type="det">
            <governor idx="11">president</governor>
            <dependent idx="10">the</dependent>
          </dep>
          <dep type="conj:and">
            <governor idx="4">born</governor>
            <dependent idx="11">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="15">States</governor>
            <dependent idx="12">of</dependent>
          </dep>
          <dep type="det">
            <governor idx="15">States</governor>
            <dependent idx="13">the</dependent>
          </dep>
          <dep type="compound">
            <governor idx="15">States</governor>
            <dependent idx="14">United</dependent>
          </dep>
          <dep type="nmod:of">
            <governor idx="11">president</governor>
            <dependent idx="15">States</dependent>
          </dep>
          <dep type="punct">
            <governor idx="4">born</governor>
            <dependent idx="16">.</dependent>
          </dep>
        </dependencies>
      </sentence>
      <sentence id="2">
        <tokens>
          <token id="1">
            <word>His</word>
            <lemma>he</lemma>
            <CharacterOffsetBegin>78</CharacterOffsetBegin>
            <CharacterOffsetEnd>81</CharacterOffsetEnd>
            <POS>PRP$</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="2">
            <word>stepfather</word>
            <lemma>stepfather</lemma>
            <CharacterOffsetBegin>82</CharacterOffsetBegin>
            <CharacterOffsetEnd>92</CharacterOffsetEnd>
            <POS>NN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="3">
            <word>is</word>
            <lemma>be</lemma>
            <CharacterOffsetBegin>93</CharacterOffsetBegin>
            <CharacterOffsetEnd>95</CharacterOffsetEnd>
            <POS>VBZ</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="4">
            <word>Lolo</word>
            <lemma>Lolo</lemma>
            <CharacterOffsetBegin>96</CharacterOffsetBegin>
            <CharacterOffsetEnd>100</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="5">
            <word>Soetoro</word>
            <lemma>Soetoro</lemma>
            <CharacterOffsetBegin>101</CharacterOffsetBegin>
            <CharacterOffsetEnd>108</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="6">
            <word>.</word>
            <lemma>.</lemma>
            <CharacterOffsetBegin>108</CharacterOffsetBegin>
            <CharacterOffsetEnd>109</CharacterOffsetEnd>
            <POS>.</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
        </tokens>
        <parse>(ROOT (S (NP (PRP$ His) (NN stepfather)) (VP (VBZ is) (NP (NNP Lolo) (NNP Soetoro))) (. .))) </parse>
        <dependencies type="basic-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="5">Soetoro</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="2">stepfather</governor>
            <dependent idx="1">His</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="5">Soetoro</governor>
            <dependent idx="2">stepfather</dependent>
          </dep>
          <dep type="cop">
            <governor idx="5">Soetoro</governor>
            <dependent idx="3">is</dependent>
          </dep>
          <dep type="compound">
            <governor idx="5">Soetoro</governor>
            <dependent idx="4">Lolo</dependent>
          </dep>
          <dep type="punct">
            <governor idx="5">Soetoro</governor>
            <dependent idx="6">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="5">Soetoro</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="2">stepfather</governor>
            <dependent idx="1">His</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="5">Soetoro</governor>
            <dependent idx="2">stepfather</dependent>
          </dep>
          <dep type="cop">
            <governor idx="5">Soetoro</governor>
            <dependent idx="3">is</dependent>
          </dep>
          <dep type="compound">
            <governor idx="5">Soetoro</governor>
            <dependent idx="4">Lolo</dependent>
          </dep>
          <dep type="punct">
            <governor idx="5">Soetoro</governor>
            <dependent idx="6">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-ccprocessed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="5">Soetoro</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="2">stepfather</governor>
            <dependent idx="1">His</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="5">Soetoro</governor>
            <dependent idx="2">stepfather</dependent>
          </dep>
          <dep type="cop">
            <governor idx="5">Soetoro</governor>
            <dependent idx="3">is</dependent>
          </dep>
          <dep type="compound">
            <governor idx="5">Soetoro</governor>
            <dependent idx="4">Lolo</dependent>
          </dep>
          <dep type="punct">
            <governor idx="5">Soetoro</governor>
            <dependent idx="6">.</dependent>
          </dep>
        </dependencies>
      </sentence>
      <sentence id="3">
        <tokens>
          <token id="1">
            <word>After</word>
            <lemma>after</lemma>
            <CharacterOffsetBegin>110</CharacterOffsetBegin>
            <CharacterOffsetEnd>115</CharacterOffsetEnd>
            <POS>IN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="2">
            <word>his</word>
            <lemma>he</lemma>
            <CharacterOffsetBegin>116</CharacterOffsetBegin>
            <CharacterOffsetEnd>119</CharacterOffsetEnd>
            <POS>PRP$</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="3">
            <word>second</word>
            <lemma>second</lemma>
            <CharacterOffsetBegin>120</CharacterOffsetBegin>
            <CharacterOffsetEnd>126</CharacterOffsetEnd>
            <POS>JJ</POS>
            <NER>ORDINAL</NER>
            <NormalizedNER>2.0</NormalizedNER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="4">
            <word>term</word>
            <lemma>term</lemma>
            <CharacterOffsetBegin>127</CharacterOffsetBegin>
            <CharacterOffsetEnd>131</CharacterOffsetEnd>
            <POS>NN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="5">
            <word>,</word>
            <lemma>,</lemma>
            <CharacterOffsetBegin>131</CharacterOffsetBegin>
            <CharacterOffsetEnd>132</CharacterOffsetEnd>
            <POS>,</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="6">
            <word>Barack</word>
            <lemma>Barack</lemma>
            <CharacterOffsetBegin>133</CharacterOffsetBegin>
            <CharacterOffsetEnd>139</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="7">
            <word>will</word>
            <lemma>will</lemma>
            <CharacterOffsetBegin>140</CharacterOffsetBegin>
            <CharacterOffsetEnd>144</CharacterOffsetEnd>
            <POS>MD</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="8">
            <word>not</word>
            <lemma>not</lemma>
            <CharacterOffsetBegin>145</CharacterOffsetBegin>
            <CharacterOffsetEnd>148</CharacterOffsetEnd>
            <POS>RB</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="9">
            <word>be</word>
            <lemma>be</lemma>
            <CharacterOffsetBegin>149</CharacterOffsetBegin>
            <CharacterOffsetEnd>151</CharacterOffsetEnd>
            <POS>VB</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="10">
            <word>president</word>
            <lemma>president</lemma>
            <CharacterOffsetBegin>152</CharacterOffsetBegin>
            <CharacterOffsetEnd>161</CharacterOffsetEnd>
            <POS>NN</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="11">
            <word>again</word>
            <lemma>again</lemma>
            <CharacterOffsetBegin>162</CharacterOffsetBegin>
            <CharacterOffsetEnd>167</CharacterOffsetEnd>
            <POS>RB</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="12">
            <word>.</word>
            <lemma>.</lemma>
            <CharacterOffsetBegin>167</CharacterOffsetBegin>
            <CharacterOffsetEnd>168</CharacterOffsetEnd>
            <POS>.</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
        </tokens>
        <parse>(ROOT (S (PP (IN After) (NP (PRP$ his) (JJ second) (NN term))) (, ,) (NP (NNP Barack)) (VP (MD will) (RB not) (VP (VB be) (NP (NN president)) (ADVP (RB again)))) (. .))) </parse>
        <dependencies type="basic-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="10">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="4">term</governor>
            <dependent idx="1">After</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="4">term</governor>
            <dependent idx="2">his</dependent>
          </dep>
          <dep type="amod">
            <governor idx="4">term</governor>
            <dependent idx="3">second</dependent>
          </dep>
          <dep type="nmod">
            <governor idx="10">president</governor>
            <dependent idx="4">term</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="5">,</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="10">president</governor>
            <dependent idx="6">Barack</dependent>
          </dep>
          <dep type="aux">
            <governor idx="10">president</governor>
            <dependent idx="7">will</dependent>
          </dep>
          <dep type="neg">
            <governor idx="10">president</governor>
            <dependent idx="8">not</dependent>
          </dep>
          <dep type="cop">
            <governor idx="10">president</governor>
            <dependent idx="9">be</dependent>
          </dep>
          <dep type="advmod">
            <governor idx="10">president</governor>
            <dependent idx="11">again</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="12">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="10">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="4">term</governor>
            <dependent idx="1">After</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="4">term</governor>
            <dependent idx="2">his</dependent>
          </dep>
          <dep type="amod">
            <governor idx="4">term</governor>
            <dependent idx="3">second</dependent>
          </dep>
          <dep type="nmod:after">
            <governor idx="10">president</governor>
            <dependent idx="4">term</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="5">,</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="10">president</governor>
            <dependent idx="6">Barack</dependent>
          </dep>
          <dep type="aux">
            <governor idx="10">president</governor>
            <dependent idx="7">will</dependent>
          </dep>
          <dep type="neg">
            <governor idx="10">president</governor>
            <dependent idx="8">not</dependent>
          </dep>
          <dep type="cop">
            <governor idx="10">president</governor>
            <dependent idx="9">be</dependent>
          </dep>
          <dep type="advmod">
            <governor idx="10">president</governor>
            <dependent idx="11">again</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="12">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-ccprocessed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="10">president</dependent>
          </dep>
          <dep type="case">
            <governor idx="4">term</governor>
            <dependent idx="1">After</dependent>
          </dep>
          <dep type="nmod:poss">
            <governor idx="4">term</governor>
            <dependent idx="2">his</dependent>
          </dep>
          <dep type="amod">
            <governor idx="4">term</governor>
            <dependent idx="3">second</dependent>
          </dep>
          <dep type="nmod:after">
            <governor idx="10">president</governor>
            <dependent idx="4">term</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="5">,</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="10">president</governor>
            <dependent idx="6">Barack</dependent>
          </dep>
          <dep type="aux">
            <governor idx="10">president</governor>
            <dependent idx="7">will</dependent>
          </dep>
          <dep type="neg">
            <governor idx="10">president</governor>
            <dependent idx="8">not</dependent>
          </dep>
          <dep type="cop">
            <governor idx="10">president</governor>
            <dependent idx="9">be</dependent>
          </dep>
          <dep type="advmod">
            <governor idx="10">president</governor>
            <dependent idx="11">again</dependent>
          </dep>
          <dep type="punct">
            <governor idx="10">president</governor>
            <dependent idx="12">.</dependent>
          </dep>
        </dependencies>
      </sentence>
      <sentence id="4">
        <tokens>
          <token id="1">
            <word>Barack</word>
            <lemma>Barack</lemma>
            <CharacterOffsetBegin>169</CharacterOffsetBegin>
            <CharacterOffsetEnd>175</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="2">
            <word>married</word>
            <lemma>marry</lemma>
            <CharacterOffsetBegin>176</CharacterOffsetBegin>
            <CharacterOffsetEnd>183</CharacterOffsetEnd>
            <POS>VBD</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="3">
            <word>Michelle</word>
            <lemma>Michelle</lemma>
            <CharacterOffsetBegin>184</CharacterOffsetBegin>
            <CharacterOffsetEnd>192</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="4">
            <word>Obama</word>
            <lemma>Obama</lemma>
            <CharacterOffsetBegin>193</CharacterOffsetBegin>
            <CharacterOffsetEnd>198</CharacterOffsetEnd>
            <POS>NNP</POS>
            <NER>PERSON</NER>
            <Speaker>PER0</Speaker>
          </token>
          <token id="5">
            <word>.</word>
            <lemma>.</lemma>
            <CharacterOffsetBegin>198</CharacterOffsetBegin>
            <CharacterOffsetEnd>199</CharacterOffsetEnd>
            <POS>.</POS>
            <NER>O</NER>
            <Speaker>PER0</Speaker>
          </token>
        </tokens>
        <parse>(ROOT (S (NP (NNP Barack)) (VP (VBD married) (NP (NNP Michelle) (NNP Obama))) (. .))) </parse>
        <dependencies type="basic-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="2">married</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="2">married</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="compound">
            <governor idx="4">Obama</governor>
            <dependent idx="3">Michelle</dependent>
          </dep>
          <dep type="dobj">
            <governor idx="2">married</governor>
            <dependent idx="4">Obama</dependent>
          </dep>
          <dep type="punct">
            <governor idx="2">married</governor>
            <dependent idx="5">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="2">married</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="2">married</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="compound">
            <governor idx="4">Obama</governor>
            <dependent idx="3">Michelle</dependent>
          </dep>
          <dep type="dobj">
            <governor idx="2">married</governor>
            <dependent idx="4">Obama</dependent>
          </dep>
          <dep type="punct">
            <governor idx="2">married</governor>
            <dependent idx="5">.</dependent>
          </dep>
        </dependencies>
        <dependencies type="collapsed-ccprocessed-dependencies">
          <dep type="root">
            <governor idx="0">ROOT</governor>
            <dependent idx="2">married</dependent>
          </dep>
          <dep type="nsubj">
            <governor idx="2">married</governor>
            <dependent idx="1">Barack</dependent>
          </dep>
          <dep type="compound">
            <governor idx="4">Obama</governor>
            <dependent idx="3">Michelle</dependent>
          </dep>
          <dep type="dobj">
            <governor idx="2">married</governor>
            <dependent idx="4">Obama</dependent>
          </dep>
          <dep type="punct">
            <governor idx="2">married</governor>
            <dependent idx="5">.</dependent>
          </dep>
        </dependencies>
      </sentence>
    </sentences>
    <coreference>
      <coreference>
        <mention representative="true">
          <sentence>1</sentence>
          <start>1</start>
          <end>3</end>
          <head>2</head>
          <text>Barack Obama</text>
        </mention>
        <mention>
          <sentence>1</sentence>
          <start>8</start>
          <end>9</end>
          <head>8</head>
          <text>he</text>
        </mention>
        <mention>
          <sentence>1</sentence>
          <start>10</start>
          <end>16</end>
          <head>11</head>
          <text>the president of the United States</text>
        </mention>
        <mention>
          <sentence>2</sentence>
          <start>1</start>
          <end>2</end>
          <head>1</head>
          <text>His</text>
        </mention>
        <mention>
          <sentence>3</sentence>
          <start>6</start>
          <end>7</end>
          <head>6</head>
          <text>Barack</text>
        </mention>
        <mention>
          <sentence>4</sentence>
          <start>1</start>
          <end>2</end>
          <head>1</head>
          <text>Barack</text>
        </mention>
      </coreference>
      <coreference>
        <mention representative="true">
          <sentence>2</sentence>
          <start>4</start>
          <end>6</end>
          <head>5</head>
          <text>Lolo Soetoro</text>
        </mention>
        <mention>
          <sentence>2</sentence>
          <start>1</start>
          <end>3</end>
          <head>2</head>
          <text>His stepfather</text>
        </mention>
        <mention>
          <sentence>3</sentence>
          <start>2</start>
          <end>3</end>
          <head>2</head>
          <text>his</text>
        </mention>
      </coreference>
    </coreference>
  </document>
</root>
			";
	  */
	}
}
