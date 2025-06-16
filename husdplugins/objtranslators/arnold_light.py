"""
copyright Ahmed Hindy. Please mention the original author if you used any part of this code
This module translates OBJ Arnold Lights into it's usd counterpart.
To use, simply drop a Scene Import (Lights) LOP node and it will import arnold lights like it does with Mantra lights.
"""
import hou
import husd
from pxr import Sdf, Gf, UsdLux


class ArnoldLightTranslator(husd.objtranslator.Translator):
    def shouldTranslateNode(self):
        self.light_enable = self._node.evalParm('light_enable')
        return self.light_enable

    def primType(self):
        self.light_type = self._node.evalParm('ar_light_type')
        self.light_type_dict = {
            0: {'prim_type': 'SphereLight',
                'usdLux_type': UsdLux.SphereLight},
            1: {'prim_type': 'DistantLight',
                'usdLux_type': UsdLux.DistantLight},
            2: {'prim_type': 'SphereLight',  # unsupported currently
                'usdLux_type': UsdLux.SphereLight},
            3: {'prim_type': 'RectLight',
                'usdLux_type': UsdLux.RectLight},
            4: {'prim_type': 'DiskLight',
                'usdLux_type': UsdLux.DiskLight},
            5: {'prim_type': 'CylinderLight',
                'usdLux_type': UsdLux.CylinderLight},
            6: {'prim_type': 'DomeLight',
                'usdLux_type': UsdLux.DomeLight},
            7: {'prim_type': 'SphereLight',  # unsupported currently
                'usdLux_type': UsdLux.SphereLight},
            8: {'prim_type': 'SphereLight',  # unsupported currently
                'usdLux_type': UsdLux.SphereLight},
        }
        return self.light_type_dict[self.light_type]['prim_type']

    def _GetprojectionType(self):
        """
        maps texture projection parm obj parm value to usd attrib value
        """
        ar_format = self._node.parm('ar_format').evalAsString()
        self.mapping_dict = {
            'mirrored_ball': 'mirroredBall',
            'angular': 'angular',
            'latlong': 'latlong',
        }
        return self.mapping_dict[ar_format]

    def populatePrim(self, prim, referenced_node_prim_paths, force_active):
        super(ArnoldLightTranslator, self).populatePrim(prim, referenced_node_prim_paths, force_active)
        usd_light = self.light_type_dict[self.light_type]['usdLux_type'](prim)
        if self.light_type == 0:
            usd_light.GetPrim().CreateAttribute('treatAsPoint', Sdf.ValueTypeNames.Bool).Set(True)

        # get attribs from obj node:
        color = self._node.evalParmTuple('ar_color')
        format = self._GetprojectionType()
        light_color_texture = self._node.parm('ar_light_color_texture').evalAsString()
        intensity = self._node.evalParm('ar_intensity')
        exposure = self._node.evalParm('ar_exposure')
        samples = self._node.evalParm('ar_samples')
        volume_samples = self._node.evalParm('ar_volume_samples')
        roundness = self._node.evalParm('ar_quad_roundness')
        soft_edge = self._node.evalParm('ar_soft_edge')
        spread = self._node.evalParm('ar_spread')
        normalize = self._node.evalParm('ar_normalize')

        camera = self._node.evalParm('ar_camera')
        diffuse = self._node.evalParm('ar_diffuse')
        specular = self._node.evalParm('ar_specular')
        transmission = self._node.evalParm('ar_transmission')
        sss = self._node.evalParm('ar_transmission')
        volume = self._node.evalParm('ar_transmission')
        indirect = self._node.evalParm('ar_indirect')
        max_bounces = self._node.evalParm('ar_max_bounces')

        # settings usd primvars:
        usd_light.CreateColorAttr().Set(Gf.Vec3f(color))
        if self.light_type == 6:  # if it's a Dome light
            usd_light.GetPrim().CreateAttribute('inputs:texture:format', Sdf.ValueTypeNames.String).Set(format)

        usd_light.GetPrim().CreateAttribute('inputs:texture:file', Sdf.ValueTypeNames.String).Set(light_color_texture)
        usd_light.CreateIntensityAttr().Set(intensity)
        usd_light.CreateExposureAttr().Set(exposure)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:samples', Sdf.ValueTypeNames.Int).Set(samples)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:volume_samples', Sdf.ValueTypeNames.Int).Set(
            volume_samples)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:roundness', Sdf.ValueTypeNames.Float).Set(roundness)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:soft_edge', Sdf.ValueTypeNames.Float).Set(soft_edge)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:spread', Sdf.ValueTypeNames.Float).Set(spread)
        usd_light.CreateNormalizeAttr().Set(normalize)

        usd_light.GetPrim().CreateAttribute('primvars:arnold:camera', Sdf.ValueTypeNames.Float).Set(camera)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:diffuse', Sdf.ValueTypeNames.Float).Set(diffuse)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:specular', Sdf.ValueTypeNames.Float).Set(specular)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:transmission', Sdf.ValueTypeNames.Float).Set(transmission)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:sss', Sdf.ValueTypeNames.Float).Set(sss)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:volume', Sdf.ValueTypeNames.Float).Set(volume)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:indirect', Sdf.ValueTypeNames.Float).Set(indirect)
        usd_light.GetPrim().CreateAttribute('primvars:arnold:max_bounces', Sdf.ValueTypeNames.Float).Set(max_bounces)


def registerTranslators(manager):
    manager.registerTranslator('arnold_light', ArnoldLightTranslator)
