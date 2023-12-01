import unittest
from unittest.mock import MagicMock, patch
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
from c5dec.core.cct import Package, PackageBuilder, AComponent, FComponent, ParaSequence, Index
from c5dec.common import C5decError


XML_STRING_EAL = '''
<eal name="structurally tested" id="eal2">
    <eal-objectives>
    <para type="normal">
        EAL2 requires the co-operation of the developer in terms of
        the delivery of design information and test results, but
        should not demand more effort on the part of the developer
        than is consistent with good commercial practise. As such it
        should not require a substantially increased investment of
        cost or time.</para>
    <para type="normal">
        EAL2 is therefore applicable in those circumstances where
        developers or users require a low to moderate level of
        independently assured security in the absence of ready
        availability of the complete development record. Such a
        situation may arise when securing legacy systems, or where
        access to the developer may be limited.</para>
    </eal-objectives>
    <eal-assurance-components>
    <para type="normal">
        EAL2 provides assurance by a full security target and an
        analysis of the SFRs in that ST, using a functional and
        interface specification, guidance documentation and a basic
        description of the architecture of the TOE, to understand the
        security behaviour.</para>
    <para type="normal">
        The analysis is supported by independent testing of the TSF,
        evidence of developer testing based on the functional
        specification, selective independent confirmation of the
        developer test results, and a vulnerability analysis (based
        upon the functional specification, TOE design, security architecture
        description and guidance evidence provided) demonstrating
        resistance to penetration attackers with a basic attack
        potential.</para>
    <para type="normal">
        EAL2 also provides assurance through use of a configuration
        management system and evidence of secure delivery
        procedures.</para>
    <para type="normal">
        This EAL represents a meaningful increase in assurance from
        EAL1 by requiring developer testing, a vulnerability analysis
        (in addition to the search of the public domain), and
        independent testing based upon more detailed TOE
        specifications.</para>
    </eal-assurance-components>
    <eal-component acomponent="ase_ccl.1"/> 
    <eal-component acomponent="ase_ecd.1"/>
    <eal-component acomponent="ase_int.1"/>
    <eal-component acomponent="ase_obj.2"/> 
    <eal-component acomponent="ase_req.2"/>
    <eal-component acomponent="ase_spd.1"/>
    <eal-component acomponent="ase_tss.1"/> 
    <eal-component acomponent="alc_cmc.2"/>
    <eal-component acomponent="alc_cms.2"/>
    <eal-component acomponent="alc_del.1"/> 
    <eal-component acomponent="adv_arc.1"/>
    <eal-component acomponent="adv_fsp.2"/>
    <eal-component acomponent="adv_tds.1"/> 
    <eal-component acomponent="agd_ope.1"/>
    <eal-component acomponent="agd_pre.1"/>
    <eal-component acomponent="ate_cov.1"/> 
    <eal-component acomponent="ate_fun.1"/>
    <eal-component acomponent="ate_ind.2"/>
    <eal-component acomponent="ava_van.2"/>
</eal>
'''

XML_STRING_CAP = '''
<cap name="Methodically composed" id="cap-b">
    <cap-objectives>
    <para type="normal">
        CAP-B permits a conscientious developer to gain maximum
        assurance from understanding, at a subsystem level, the
        affects of interactions between component TOEs integrated in
        the composed TOE, whilst minimising the demand of involvement
        of the base component developer.</para>
    <para type="normal">
        CAP-B is applicable in those circumstances where developers or
        users require a moderate level of independently assured
        security, and require a thorough investigation of the composed
        TOE and its development without substantial
        re-engineering.</para>
    </cap-objectives>
    <cap-assurance-components>
    <para type="normal">
        CAP-B provides assurance by analysis of a full security target
        for the composed TOE.  The SFRs in the composed TOE ST are
        analysed using the outputs from the evaluations of the
        component TOEs (e.g. ST, guidance documentation), a
        specification for the interfaces between the component TOEs
        and the TOE design (describing TSF subsystems) contained in
        the composed development information to understand the
        security behaviour.</para>
    <para type="normal">
        The analysis is supported by independent testing of the
        interfaces of the base component that are relied upon by the
        dependent component, as described in the reliance information
        (now also including TOE design), evidence of developer testing
        based on the reliance information, development information and
        composition rationale, and selective independent confirmation
        of the developer test results.  The analysis is also supported
        by a vulnerability analysis of the composed TOE by the
        evaluator demonstrating resistance to attackers with basic
        attack potential.</para>
    <para type="normal">
        This CAP represents a meaningful increase in assurance from
        CAP-A by requiring more complete testing coverage of the
        security functionality.</para>
    </cap-assurance-components>  
    <cap-component acomponent="ase_ccl.1"/> 
    <cap-component acomponent="ase_ecd.1"/>
    <cap-component acomponent="ase_int.1"/>
    <cap-component acomponent="ase_obj.2"/> 
    <cap-component acomponent="ase_req.2"/>
    <cap-component acomponent="ase_tss.1"/>
    <cap-component acomponent="ase_spd.1"/> 
    <cap-component acomponent="alc_cmc.1"/>
    <cap-component acomponent="alc_cms.2"/>
    <cap-component acomponent="agd_pre.1"/> 
    <cap-component acomponent="agd_ope.1"/>
    <cap-component acomponent="aco_cor.1"/>
    <cap-component acomponent="aco_dev.2"/> 
    <cap-component acomponent="aco_ctt.2"/>
    <cap-component acomponent="aco_vul.2"/>
    <cap-component acomponent="aco_rel.1"/>
</cap>
'''

class TestPackage(unittest.TestCase):


    def setUp(self):
        self.package = Package(_id="Pkg1", _name="Pkg_name")
        self.package.acronym = "Pkg"
        self.package.objectives = MagicMock(ParaSequence())
        self.package.assurance_components = MagicMock(ParaSequence())
        pkg_comp = MagicMock(AComponent(_id="comp_id", _name="comp"))
        Index.update(pkg_comp._id, pkg_comp)
        self.package.children = [pkg_comp]


    def test_is_valid_success(self):
        self.assertTrue(self.package.is_valid())

    def test_multiple_child_types_raises_error(self):
        self.package.children.append("InvalidCompID")
        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_non_uniform_components_raises_error(self):
        fcomp = MagicMock(FComponent(_id="fcomp1", _name="fcomp"))
        acomp = MagicMock(AComponent(_id="acomp1", _name="acomp"))
        Index.update(fcomp._id, fcomp)
        Index.update(acomp._id, acomp)
        self.package.children = [fcomp, acomp]

        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_non_component_type_raises_error(self):
        # tests that children/components must be of type AComponent or FComponent
        para = MagicMock(ParaSequence())
        para._id = "para_id"
        Index.update(para._id, para)
        self.package.children = [para]

        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_non_correspondant_id_raises_error(self):
        # tests that string input must correspond to AComponent or FComponent obj.
        para = MagicMock(ParaSequence())
        para._id = "NotComponentID"
        Index.update(para._id, para)
        self.package.children = ["NotComponentID"]

        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_not_updated_index_raises_error(self):
        acomp = MagicMock(AComponent(_id="NotUpdatedId", _name="comp1"))
        self.package.children = [acomp]

        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_missing_objectives_raises_error(self):
        self.package.objectives = None
        with self.assertRaises(C5decError):
            self.package.is_valid()

    def test_missing_assurance_components_raises_error(self):
        self.package.assurance_components = None
        with self.assertRaises(C5decError):
            self.package.is_valid()
    
    def tearDown(self):
        Index.clear()


class TestPackageBuilder(unittest.TestCase):

    def setUp(self):
        self.package = Package(_id="Pkg1", _name="Pkg_name")
        self.package.acronym = "Pkg"
        self.builder = PackageBuilder(self.package)

    def test_initialization(self):
        self.assertIsInstance(self.builder.instance, Package)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            PackageBuilder("INVALIDELEMENT")

    def test_build_attributes(self):
        xml_string = '''
        <pkg id="pkg2" name="pkg_name">
            Package Content.
        </pkg>
        '''
        parent_obj = MagicMock()
        node = etree.fromstring(xml_string)

        self.builder._build_attributes(node, parent_obj=parent_obj)

        self.assertEqual(self.package._id, "pkg2")
        self.assertEqual(self.package._name, "pkg_name")
        self.assertEqual(self.package.acronym, "pkg")
        self.assertEqual(self.package.parent, parent_obj)

    @patch.object(ParaSequence, "build")
    def test_build_children_parasequence(self, mock_parasequence_build):
        xml_string = '''
        <Pkg name="Methodically composed" id="cap-b">
            <Pkg-objectives>
                Objectives.
            </Pkg-objectives>
            <Pkg-assurance-components>
                Assurance Components.
            </Pkg-assurance-components>
        </Pkg>
        '''
        node = etree.fromstring(xml_string)
        mocked_parasequence = []
        for child in node:
            self.builder._build_children(child)
            mocked_parasequence.append(mock_parasequence_build(child))

        self.assertEqual(mocked_parasequence, self.package.container)

    def test_build_children_component(self):
        xml_string = '''
        <Pkg>
            <Pkg-component acomponent="Comp_Id"/>
            <Pkg-component acomponent="Comp_Id1"/>
        </Pkg>
        '''
        node = etree.fromstring(xml_string)
        for child in node:
            self.builder._build_children(child)
        
        self.assertEqual(self.package.children, ["Comp_Id", "Comp_Id1"])



if __name__ == "__main__":
    unittest.main()