<?php

namespace App\DataFixtures;

use App\Entity\Camera;
use App\Entity\Segment;
use App\Entity\Shop;
use App\Utility\DataObject\ImageManipulationSettings;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;

class AppFixtures extends Fixture
{
    public function load(ObjectManager $manager)
    {
        $segmentQuickSnacks = new Segment();
        $segmentQuickSnacks->setName('Szybkie przekąski');
        $segmentQuickSnacks->setType(SegmentType::QUICK_SNACK);
        $manager->persist($segmentQuickSnacks);

        $segmentReadyMeals = new Segment();
        $segmentReadyMeals->setName('Dania Gotowe');
        $segmentReadyMeals->setType(SegmentType::READY_MEAL);
        $manager->persist($segmentReadyMeals);

        $segmentGrills = new Segment();
        $segmentGrills->setName('Grille/Rollery');
        $segmentGrills->setType(SegmentType::GRILL);
        $manager->persist($segmentGrills);

        $manager->flush();
        
        for ($i=0;$i<10;$i++) {
            $shop = new Shop();
            $shop->setName('Testowy sklep' . $i);
            $shop->setCode(uniqid('sk-ziel-'));

            $manager->persist($shop);

            $caseCamera = new Camera();
            $caseCamera->setType('dahua');
            $caseCamera->setIp('172.16.1.' . $i);
            $caseCamera->setShop($shop);
            $caseCamera->setManipulationSettings($this->generateImageManipulationSettings());
            if ($i%2==0) {
                $caseCamera->setSegment($segmentQuickSnacks);
            } else {
                $caseCamera->setSegment($segmentGrills);
            }
            $manager->persist($caseCamera);

            $grillCamera = new Camera();
            $grillCamera->setType('dahua');
            $grillCamera->setIp('172.16.2.' . $i);
            $grillCamera->setShop($shop);
            $grillCamera->setSegment($segmentGrills);

            $grillCamera->setManipulationSettings($this->generateImageManipulationSettings());

            $manager->persist($grillCamera);
        }

        $manager->flush();
    }
    
    private function generateImageManipulationSettings(): ImageManipulationSettings
    {
        $manipulationsSettings = new ImageManipulationSettings();
        $manipulationsSettings->cropX = rand(5, 50);
        $manipulationsSettings->cropY = rand(5, 50);
        $manipulationsSettings->cropHeight = rand(100,600);
        $manipulationsSettings->cropWidth = rand(100,600);
        $manipulationsSettings->rotateAngle = round(((float) rand(1,80)) * 1.16, 2);
        return $manipulationsSettings;
    }
}
