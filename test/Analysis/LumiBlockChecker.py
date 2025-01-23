import json
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from functools import singledispatchmethod




@dataclass
class LumiBlockChecker:
    """
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile
    """
    cert: dict[np.uint32, npt.NDArray[np.uint32]]

    @staticmethod
    def _transform_lumi_ranges(lumi: list[tuple[int, int]]
    ) -> npt.NDArray[np.uint32]:
        """
        """
        flat_lumi = np.array(lumi, dtype=np.uint32).flatten()
        # [first, last] to (first, last]
        flat_lumi[::2] -= 1
        return flat_lumi

    @classmethod
    def from_dict(cls, cert: dict[int, list[tuple[int, int]]]):
        flat_cert = {np.uint32(run): cls._transform_lumi_ranges(lumi_ranges)
                     for run, lumi_ranges in cert.items()}
        return cls(flat_cert)

    @classmethod
    def from_json(cls, path):
        with open(path) as stream:
            cert = json.load(stream)
        return cls.from_dict(cert)

    @staticmethod
    def _get_lumi_mask(lumi_arr: npt.NDArray[np.uint32],
                     ranges: npt.NDArray[np.uint32]
    ) -> npt.NDArray[np.bool_]:
        """
        """
        # odd(even) indices indicate good(bad) lumi blocks
        indices = np.searchsorted(ranges, lumi_arr)
        mask = (indices & 0x1).astype(bool)
        return mask

    @singledispatchmethod
    def get_lumi_mask(self, run, lumi: npt.NDArray[np.uint32]):
        raise NotImplementedError(f'expected np.uint32, npt.NDArray[np.uint32]'
                                  f' or int but got {type(run)}')

    @get_lumi_mask.register(int)
    @get_lumi_mask.register(np.uint32)
    def _(self,
          run: np.uint32,
          lumi: npt.NDArray[np.uint32]
    ) -> npt.NDArray[np.bool_]:
        """
        """
        if isinstance(run, int):
            run = np.uint32(run)

        if run in self.cert:
            mask = self._get_lumi_mask(lumi, ranges=self.cert[run])
        else:
            mask = np.full_like(lumi, fill_value=False, dtype=bool)
        return mask

    @get_lumi_mask.register(np.ndarray)
    def _(self,
          run: npt.NDArray[np.uint32],
          lumi: npt.NDArray[np.uint32]
    ) -> npt.NDArray[np.bool_]:
        """
        """
        mask = np.full_like(lumi, fill_value=False, dtype=bool)
        for each in np.unique(run):
            run_mask = run == each
            mask[run_mask] = self.get_lumi_mask(each, lumi[run_mask])
        return mask