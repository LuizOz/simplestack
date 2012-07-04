# Copyright 2012 Locaweb.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# @author: Francisco Freire, Locaweb.
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

from simplestack.exceptions import FeatureNotImplemented
from simplestack.views.format_view import FormatView


class SimpleStack(object):

    def __init__(self):
        self.connection = False
        self.format_for = FormatView()

    def libvirt_connect(self):
        raise FeatureNotImplemented()

    def connect(self):
        raise FeatureNotImplemented()

    def pool_info(self):
        raise FeatureNotImplemented()

    def guest_list(self):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        not_running = [
            self.libvirt_vm_info(self.libvirt_connection.lookupByName(vm_name))
            for vm_name in self.libvirt_connection.listDefinedDomains()
        ]
        running = [
            self.libvirt_vm_info(self.libvirt_connection.lookupByID(vm_id))
            for vm_id in self.libvirt_connection.listDomainsID()
        ]
        return not_running + running

    def guest_create(self, guestdata):
        raise FeatureNotImplemented()

    def guest_import(self, gueststream, guestsize):
        raise FeatureNotImplemented()

    def guest_info(self, guest_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return self.libvirt_vm_info(dom)

    def guest_shutdown(self, guest_id, force=False):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        if force:
            return dom.destroy()
        else:
            return dom.shutdown()

    def guest_start(self, guest_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        dom.create()

    def guest_suspend(self, guest_id):
        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return dom.suspend()

    def guest_resume(self, guest_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        return dom.resume()

    def guest_reboot(self, guest_id, force=False):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        if force:
            return vm.reset(0)
        else:
            return vm.reboot(0)

    def guest_update(self, guest_id, guestdata):
        raise FeatureNotImplemented()

    def guest_delete(self, guest_id):
        raise FeatureNotImplemented()

    def media_mount(self, guest_id, media_data):
        raise FeatureNotImplemented()

    def media_info(self, guest_id):
        raise FeatureNotImplemented()

    def network_interface_list(self, guest_id):
        raise FeatureNotImplemented()

    def network_interface_info(self, guest_id, network_interface_id):
        raise FeatureNotImplemented()

    def snapshot_list(self, guest_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByID(guest_id)
        snaps = [
            self.libvirt_snapshot_info(s)
            for s in dom.snapshotListNames()
        ]
        return snaps

    def snapshot_create(self, guestname, name=None):
        raise FeatureNotImplemented()

    def snapshot_info(self, guestname, snapshot_name):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        if snap:
            return self.libvirt_snapshot_info(snap)
        else:
            raise EntityNotFound("Snapshot", snapshot_id)

    def snapshot_delete(self, guest_id, snapshot_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        snap.delete(0)

    def snapshot_revert(self, guest_id, snapshot_id):
        if not self.has_libvirt():
            raise FeatureNotImplemented()

        dom = self.libvirt_connection.lookupByUUIDString(guest_id)
        snap = self.libvirt_get_snapshot(dom, snapshot_id)
        dom.revertToSnapshot(snap)

    def tag_list(self, guest_id):
        raise FeatureNotImplemented()

    def tag_create(self, guest_id, tag_name):
        raise FeatureNotImplemented()

    def tag_delete(self, guest_id, tag_name):
        raise FeatureNotImplemented()

    def libvirt_vm_info(self, dom):
        infos = dom.info()
        return (
            self.format_for.guest(
                dom.UUIDString(),
                dom.name(),
                infos[3],
                infos[1] / 1024,
                None, None,
                self.state_translation[infos[0]],
            )
        )

    def libvirt_snapshot_info(self, snapshot):
        return (
            self.format_for.snapshot(
                snapshot.get_description(),
                snapshot.name(),
                snapshot.get_state(),
                snapshot.get_path(),
                snapshot.get_create_time()
            )
        )

    def libvirt_get_snapshot(self, dom, snapshot_id):
        pass

    def has_libvirt(self):
        return hasattr(self, "libvirt_connection") and self.libvirt_connection